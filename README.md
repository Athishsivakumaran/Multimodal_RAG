# Multimodal RAG: Chat with Your Documents (Text, Images, Tables)

## 🚀 Overview
This project is a **Multimodal Retrieval-Augmented Generation (RAG) System** that allows users to **upload PDFs and PPTs**, extract insights from text, images, and tables, and interact with them through a chatbot interface. Built with **Streamlit and Google Gemini AI**, it provides a powerful way to query and analyze documents.

## 🌟 Features
- **Handles Text, Images, and Tables** from PDFs and PPTs
- **Summarizes Documents** using **Gemini API (Flash 2.0)**
- **Retrieves Top 5 Matching Results** using **RAG Fusion**
- **Displays Responses with Relevant Tables & Diagrams**
- **Interactive Chat UI** built with Streamlit

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python (FastAPI)
- **AI Models:** Google Gemini Flash 2.0 & Text-Embedding-004
- **Document Processing:** Unstructured Library
- **Vector Storage:** FAISS or ChromaDB

## 🔄 Workflow
1. **Upload PDFs or PPTs** 📂
2. **Extract Text (Chunking with Titles), Images, and Tables** 📝
3. **Summarize Content** using **Gemini API (Flash 2.0)** ✨
4. **Generate Embeddings** using **Gemini API text-embedding-004** 🔢
5. **User Asks a Question** ❓
6. **Retrieve Best Results Using RAG Fusion (Retriever + LLM)** 🎯
7. **Send Top 5 Documents (Text, Images, Tables) to LLM** 🧠
8. **Display Response in Streamlit UI** 💡

## 🔧 Installation
1. **Clone the repository**
   ```sh
   git clone(https://github.com/Athishsivakumaran/Multimodal_RAG.git
   cd multimodal-rag
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Streamlit app**
   ```sh
   streamlit run app.py
   ```

## 🖥️ Usage
1. Open the app in your browser.
2. Upload a **PDF or PPT** file.
3. Ask questions related to the document.
4. Get **instant responses** with text, images, and tables.

## 🎯 Use Cases
### 💼 Business Owners & Analysts:
Ever needed to check a **balance sheet** or track **revenue trends** in a giant annual report? Instead of flipping through pages, just ask—and get the tables, visuals, and an **in-depth analysis instantly**. 📊

### 🎓 Students & Researchers:
Exam tomorrow? Need a **definition AND its diagram** from a 50-slide lecture? Just type your question, and it pulls both—plus a **detailed explanation** so you actually understand it (not just memorize it).

### 📑 Anyone Drowning in Documents:
Legal agreements, policies, research papers—this doesn’t just fetch information, it **breaks it down for you**. Forget endless scrolling. Just ask, get answers, and move on.

This isn’t just AI—it’s **your personal document assistant**.

## 🤝 Contributing
We welcome contributions! Feel free to **submit issues, create pull requests, or suggest improvements.** 🚀

## 📜 License
This project is licensed under the **MIT License**.

---

### 📩 Questions or Feedback?
Feel free to reach out or open an issue! Let's make document analysis **smarter and faster**. 🚀

