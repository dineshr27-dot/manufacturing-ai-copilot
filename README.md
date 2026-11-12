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
7. The generated answer and source references are displayed in the web interface.

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

For local network access, start the application with:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `http://YOUR-LAPTOP-IP:8000` on a mobile device connected to the same accessible local network.

## Five Original Test Questions and Application Answers

The following five questions were created to test the application's ability to retrieve information from the provided manufacturing manuals and SOP documents.

### Question 1: Coolant Concentration

**Question:** What is the recommended coolant concentration for the TX-200 CNC turning centre?

**Application Answer:** The recommended coolant concentration is 6–8%.

**Source:** MNT-MAN-CNC-02_TX-200_Preventive_Maintenance.pdf, Page 1.

### Question 2: Machine Alarm AL-104

**Question:** The machine is showing alarm AL-104. What does it mean and what should the operator do?

**Application Answer:** AL-104 indicates low way lubrication. The operator should top up the ISO VG68 way lubricant to the MAX level and press RESET.

**Source:** MNT-MAN-CNC-02_TX-200_Preventive_Maintenance.pdf, Page 2.

### Question 3: Lockout/Tagout Safety

**Question:** Who is allowed to remove a lockout lock from a machine?

**Application Answer:** Each authorized person must remove their own personal lock. Another person must not remove that person's lock under the normal lock-removal procedure.

**Source:** SAF-SOP-003_Lockout_Tagout_Procedure.pdf.

### Question 4: BH-220 Outer Diameter Tolerance

**Question:** What is the outer diameter tolerance for the BH-220 bearing housing?

**Application Answer:** The outer diameter is 90.000 ± 0.050 mm.

**Source:** QC-SOP-014 Rev04 Incoming Material Inspection, Page 2.

### Question 5: Spindle Runout Maintenance

**Question:** How often should spindle runout be checked, and who does it?

**Application Answer:** Spindle runout should be checked monthly by the Maintenance technician.

**Source:** MNT-MAN-CNC-02_TX-200_Preventive_Maintenance.pdf, Page 1.

## Testing Summary

| Test | Expected result |
|---|---|
| Coolant concentration | 6–8% |
| Alarm AL-104 | Top up ISO VG68 to MAX and press RESET |
| Lockout lock removal | Each authorized person removes their own lock |
| BH-220 outer diameter | 90.000 ± 0.050 mm |
| Spindle runout | Monthly, Maintenance technician |

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
