from frontend_modules.state_manager import st, add_message
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
def display_chat_input():
    """Display the chat input field"""
    # Create a form to prevent auto-rerun
    with st.form(key="chat_form"):
        user_input = st.text_input(
            "Ask a question about your documents", 
            key="user_input", 
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("Send")
    
    # Only process when the form is submitted
    if submit_button and user_input:
        # Add user message to chat
        add_message("user", user_input)
        
        # Process the user input
        with st.spinner("Generating response..."):
            process_user_input(user_input)
        
        # Force a rerun to display the response immediately
        st.rerun()

def process_user_input(user_input):
    """Process user input without causing reruns"""
    try:
        # Ensure chain is initialized
        if "chain" not in st.session_state or st.session_state.chain is None:
            add_message("assistant", "Sorry, the chat system isn't ready yet. Please try again later.")
            return
        
        # Invoke the chain
        response = st.session_state.chain.invoke(user_input)
        print("DEBUG: Chain response:", response)  # Log the raw response
        
        # Extract structured components
        answer_text = response.answer
        images = response.images
        tables = response.tables

        print("DEBUG: Extracted response components:", answer_text, images, tables)  # Log extracted components

        # Format output beautifully
        structured_response = format_response(answer_text, images, tables)

        # Display formatted response
        add_message("assistant", structured_response)


    
    except Exception as e:
        print(f"Full error: {repr(e)}")  # Log complete error details
        add_message("assistant", "An error occurred while processing your request.")


def format_response(text, images, tables):
    """Builds a formatted HTML string for the response"""
    response_html = ""

    # 1️⃣ Add text content
    if text:
        response_html += f"<div class='text-content'>{text}</div>"

    # 2️⃣ Add images (base64 handling remains the same)
    if images:
        for i, image_base64 in enumerate(images):
            response_html += f"""
            <figure>
                <img src="data:image/png;base64,{image_base64}" alt="Figure {i+1}">
                <figcaption>Figure {i+1}</figcaption>
            </figure>
            """

    # 3️⃣ Add tables
    if tables:
        for i, table_html in enumerate(tables):
            response_html += f"""
            <div class='table-wrapper'>
                <h4>Table {i+1}</h4>
                {table_html}
            </div>
            """

    return response_html
  

def html_table_to_dataframe(html):
    """Converts an HTML table into a Pandas DataFrame"""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    
    if not table:
        return pd.DataFrame()  # Return an empty dataframe if no table found

    # Extract table headers
    headers = [th.text.strip() for th in table.find_all("th")]

    # Extract table rows
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = [td.text.strip() for td in tr.find_all("td")]
        rows.append(cells)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df


