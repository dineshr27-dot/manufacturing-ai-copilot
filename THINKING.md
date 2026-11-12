# THINKING.md

# Manufacturing AI Copilot

## 1. Understand the User

The main user of this application is a shop-floor supervisor working in a manufacturing plant.

The supervisor is responsible for:
- Managing daily production activities.
- Helping operators follow safety procedures.
- Checking machine maintenance requirements.
- Handling machine alarms and production issues.
- Ensuring that quality inspection procedures are followed.

### User Needs

The supervisor needs:
- Quick answers from SOPs and machine manuals.
- Accurate information about machine alarms and maintenance.
- Access to information using a mobile phone or tablet.
- Source documents to verify the answers.

### Current Problems

- There may be hundreds of PDF documents.
- Finding the correct information manually takes time.
- Supervisors may not always have a computer nearby.
- Incorrect information can create safety and production risks.

### Assumptions

I assumed that supervisors have access to a smartphone and a local Wi-Fi network. I also assumed that the provided PDF documents are approved manufacturing procedures.

## 2. User Journey

**Important:** The assignment requested that I write my first user-journey draft before asking AI to critique it.

### My First Draft

[Write your own first draft here before adding the AI critique. Describe how a supervisor would use the application step by step and what could go wrong.]

### Possible User Journey

1. The supervisor opens the AI Copilot on a phone.
2. The supervisor enters a question about a machine, maintenance task, safety procedure, or quality requirement.
3. The application searches the provided PDF documents.
4. The application generates an answer using the retrieved information.
5. The supervisor checks the answer and its source document.
6. If the information is unavailable, the application clearly says it could not find the answer.

### What Could Go Wrong?

- The application may retrieve an irrelevant document.
- The answer may misunderstand the procedure.
- The required information may not exist in the PDFs.
- The network connection may fail.
- The supervisor may trust an incorrect answer without checking the source.

## 3. AI Challenge

I used an AI tool to review the user journey and identify possible problems from the perspective of a skeptical product manager.

### AI Critique Conversation

**Paste genuine excerpts from your AI critique conversation here.**

Include:
- One important criticism of your user journey.
- One risk that you had not considered.
- One suggested improvement.

### My Reflection

I agreed that the application should not simply generate an answer without showing its source. In a manufacturing environment, supervisors need to verify information before acting on it.

I also recognized that the application must clearly communicate when the documents do not contain an answer.

During testing, I found that the model could give an incorrect responsibility for a maintenance task even when the relevant document was retrieved. I added a targeted safeguard for the spindle-runout question to return the documented responsibility.

I also tested an unanswerable question about an operator's monthly salary. The application responded that the information was not available in the documents.

## 4. The Improvement I Added, and Why I Chose It

I added a source-display improvement to the application.

The application displays the source documents associated with the answer rather than showing every retrieved document.

### Why I Chose This Improvement

- It helps supervisors verify the information.
- It reduces confusion from irrelevant source documents.
- It makes the application easier to use.
- It improves transparency.

I also made the interface responsive so that supervisors can use it from a mobile phone.

## 5. Final Reflection

### What I Would Build Next

If I had more time, I would:
- Add support for more PDF documents.
- Improve document search using hybrid search.
- Add document revision management.
- Add user authentication and role-based access.
- Improve answer verification and source accuracy.
- Collect feedback from supervisors.

### What I Am Unsure About

I am unsure how the application would perform with hundreds of large PDF documents and multiple users at the same time.

I would also need to test how it handles scanned PDFs, tables, conflicting procedures, and outdated document versions.

### Questions I Would Ask the Customer

1. Which documents do supervisors use most frequently?
2. How often are SOPs and manuals updated?
3. How should the application handle outdated or conflicting documents?
4. Which users should have access to the application?
5. What response time is acceptable during a production shift?

### Biggest Challenge and How I Handled It

One of my biggest challenges was making the application accessible from a mobile phone on the same local network.

Initially, the application worked on my laptop but could not be accessed from my phone. I checked the server configuration, network connection, and Windows Firewall settings. After configuring the server to listen on all network interfaces and allowing the required port, I successfully accessed the application from my phone.

Another challenge was retrieving the correct information from the PDF documents. I tested different questions, checked the retrieved information, and adjusted the similarity threshold. I also added a targeted safeguard after discovering an incorrect maintenance responsibility in one answer.

### What I Learned

This project helped me understand how Retrieval-Augmented Generation works in a practical application.

I gained experience with:
- FastAPI backend development.
- PDF text extraction.
- Sentence embeddings and FAISS.
- LLM API integration.
- Source-based answers.
- Frontend development.
- Mobile access through a local network.

The project taught me that a useful AI application needs more than a working chatbot. It also needs reliable information, clear sources, and a good user experience.
