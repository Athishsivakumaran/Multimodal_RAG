
import json
from typing import List
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import List

class LLMResponse(BaseModel):
    answer: str
    images: List[str]  
    tables: List[str] 

def parse_docs(docs):
    """
    Parses the documents to extract text, tables, and images.
    """
    for doc in docs:
        print(doc.metadata.get("type"))
    parsed_docs = {"images": [], "texts": [], "tables": []}
    for doc in docs:
        parsed_docs[doc.metadata.get("type")+"s"].append(doc)
    return parsed_docs
import json

def parse_llm_response(response,images, tables):
    """Parses the raw LLM response into structured JSON format."""
    try:
        # Extract only JSON from the response (remove markdown formatting like ```json ... ```)
        response_text = response.content.strip("```json\n").strip("```")
        
        # Parse the response into a Python dictionary
        parsed_data = json.loads(response_text)

        # Convert the dictionary into an LLMResponse object
        return LLMResponse(
            answer=parsed_data.get("answer", ""),
            images=[image.page_content for image in images],  # Pass extracted images
            tables=[table.page_content for table in tables]   # Pass extracted tables
        )
    
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None  # Handle gracefully if the response isn't valid JSON



def generate_response(retriever):
    def build_prompt(kwargs):
        docs_by_type = kwargs["context"]
        user_question = kwargs["question"] 

        context_text = ""
        if len(docs_by_type["texts"]) > 0:
            for text_element in docs_by_type["texts"]:
                context_text += text_element.page_content
            
        context_tables = ""
        if len(docs_by_type["tables"]) > 0:
            for i, table_element in enumerate(docs_by_type["tables"]):
                table_num = i + 1
                context_tables += f"\n\n[Table {table_num}]:\n{table_element.page_content}\n"
        
       
        prompt_template = f"""
        You are an advanced AI assistant designed to answer questions based on a combination of text, tables, and images. 
        Your task is to carefully analyze the provided context—comprising of texts, tables, and images—and generate a detailed, accurate, 
        and well-cited answer based on that context. Carefully analyze the information provided before generating your response.

        **Context (Textual Information):**
        {context_text}

        **Context (Tabular Information - Raw HTML Data):**
        {context_tables}

        **Context (Images Included Below - Use these in analysis if referenced)**

       **Task:**
        - Provide detailed explanations and answers to the user's question.
        - Always cite your sources when referring to specific content, using the citation labels provided above.
        - When referencing an image or a table use the citations given
        - Perform in-depth analysis of any tables or images relevant to the question:
        - For tables: Analyze trends, patterns, outliers, and key data points. Explain the significance of the data in relation to the question and how it supports your answer. Consider relationships between different columns/rows and what insights they reveal.
        - For images: Provide a comprehensive description of what you see, including key features, elements, patterns, relationships, and any text or data visualizations within the image. Explain how specific elements in the image directly relate to the question.
        - Explicitly connect your analysis of tables and images to the user's question, showing how they provide evidence for your answer.
        - When multiple tables or images are available, compare and contrast their content where relevant.
        - If the answer draws from multiple sources (text, tables, and images), explain how these different sources complement each other to provide a comprehensive answer.
        - Ensure your response is formatted as valid JSON as specified below.

        
        **Question:**
        {user_question}
        """

        

        # Fix 4: Proper message structure
        prompt_content = [{"type": "text", "text": prompt_template}]

        # Add images correctly
        if len(docs_by_type["images"]) > 0:
            for i, image in enumerate(docs_by_type["images"]):
                image_num = i + 1
                prompt_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image.page_content}"},
                    }
                )
                # Add a text label after each image for clarity
                prompt_content.append(
                    {"type": "text", "text": f"[This is Fig. {image_num}]"}
                )



        return [HumanMessage(content=prompt_content)]

    chain = (
    {
        "context": retriever | RunnableLambda(parse_docs),
        "question": RunnablePassthrough(),
    }
    | RunnableLambda(lambda kwargs: {
        "prompt": build_prompt(kwargs),
        "images": kwargs["context"]["images"], 
        "tables": kwargs["context"]["tables"] 
    })
    | RunnableLambda(lambda kwargs: {
        "response": ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5).invoke(kwargs["prompt"]),
        "images": kwargs["images"],
        "tables": kwargs["tables"]
    })
    | RunnableLambda(lambda kwargs: parse_llm_response(kwargs["response"], kwargs["images"], kwargs["tables"]))  # Final structured response
)

    return chain