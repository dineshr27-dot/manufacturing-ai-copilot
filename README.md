# Manufacturing AI Copilot

An AI-powered chatbot that helps manufacturing shop-floor supervisors quickly find reliable answers from machine manuals and Standard Operating Procedures (SOPs).

## Project Overview

Manufacturing plants use multiple PDF manuals and SOP documents for machine maintenance, safety procedures, and quality inspection.

Finding the correct information manually can take time, especially when supervisors need quick answers on the shop floor.

Manufacturing AI Copilot uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from provided PDF documents and generate answers with source references.

## Features

- Ask questions about manufacturing manuals and SOPs.
- Retrieve relevant information from PDF documents.
- Generate answers using an LLM.
- Display source document names and page numbers.
- Provide answers based on the available documents.
- Indicate when the requested information is not available.
- Responsive web interface for laptop and mobile devices.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| LangChain / RAG components | Retrieval workflow |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Groq API | LLM-powered answer generation |
| HTML | Web page structure |
| CSS | Responsive styling |
| JavaScript | Frontend interactions |
| PyPDF | PDF text extraction |

## Project Architecture

1. PDF documents are loaded and their text is extracted.
2. The extracted text is divided into smaller chunks.
3. Sentence Transformers generate embeddings.
4. FAISS stores and retrieves relevant document chunks.
5. The user's question is converted into an embedding.
6. Relevant chunks are passed to the Groq LLM.
7. The generated answer and available source references are displayed in the web interface.

## Project Structure

```text
manufacturing-ai-copilot/
│
├── app/
│   ├── config.py
│   ├── ingestion.py
│   └── rag.py
│
├── data/
│   └── PDF documents
│
├── vectorstore/
│   └── FAISS index and stored chunks
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── THINKING.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/manufacturing-ai-copilot.git
cd manufacturing-ai-copilot
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Never upload your actual API key to GitHub.

### 5. Run the application

```bash
uvicorn main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

The application also supports local network access when the server is started with:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `http://YOUR-LAPTOP-IP:8000` on a mobile device connected to the same accessible local network.

## Sample Questions

Try asking:

1. What is the required coolant concentration?
2. How often should spindle runout be checked, and who is responsible?
3. What is the acceptable outer diameter tolerance for BH-220?
4. What should an operator do when alarm AL-104 occurs?
5. What is the monthly salary of a machine operator?

The last question is intentionally outside the provided documents. The chatbot should indicate that the information is unavailable.

## Expected Results

- Coolant concentration: 6–8%.
- Spindle runout: Monthly, checked by the Maintenance technician.
- BH-220 outer diameter: 90.000 ± 0.050 mm.
- AL-104: Top up ISO VG68 way lubricant to MAX and press RESET.
- Machine operator salary: Not available in the provided documents.

## Limitations

- Answers depend on the quality and completeness of the provided PDF documents.
- Retrieval may return irrelevant document chunks.
- LLM-generated answers should be verified against the original SOPs, especially for safety-critical procedures.
- A valid Groq API key and the required vector index are needed to run the application.

## Future Improvements

- Add more manufacturing manuals and SOPs.
- Improve retrieval accuracy and source validation.
- Add document version management.
- Improve mobile usability.
- Add user authentication and access control.

## Author

**Dinesh R**

B.Sc. Computer Science – Artificial Intelligence and Machine Learning

## License

Add a license only if you have selected one for this project.
