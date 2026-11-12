
const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

// Display answer text with safe bold formatting
function formatAnswer(paragraph, text) {
    const parts = text.split(/(\*\*.*?\*\*)/gs);

    parts.forEach(part => {
        if (part.startsWith("**") && part.endsWith("**")) {
            const bold = document.createElement("strong");
            bold.textContent = part.slice(2, -2);
            paragraph.appendChild(bold);
        } else {
            paragraph.appendChild(document.createTextNode(part));
        }
    });
}

// Add a message to the chat
function addMessage(text, type, sources = []) {
    const message = document.createElement("div");

    message.className = type === "user"
        ? "user-message"
        : "assistant-message";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = type === "user" ? "You" : "AI";

    const content = document.createElement("div");
    content.className = "message-content";

    const heading = document.createElement("strong");
    heading.textContent = type === "user"
        ? "Your Question"
        : "Manufacturing AI Copilot";

    const paragraph = document.createElement("p");
    formatAnswer(paragraph, text);

    content.appendChild(heading);
    content.appendChild(paragraph);

    // Find source IDs cited in the AI answer.
    // Supports both [S1] and 【S1】 formats.
    const citedIds = [
        ...new Set(
            [...text.matchAll(/[【\[]\s*(S\d+)\s*[】\]]/g)]
                .map(match => match[1])
        )
    ];

    // Display only sources actually cited in the answer.
    const relevantSources = sources.filter(source =>
        citedIds.includes(source.id)
    );

    // Display relevant PDF sources
    if (relevantSources.length > 0) {
        const sourceBox = document.createElement("div");
        sourceBox.className = "sources";

        const sourceHeading = document.createElement("strong");
        sourceHeading.textContent = "Source Documents";

        sourceBox.appendChild(sourceHeading);

        relevantSources.forEach(source => {
            const item = document.createElement("div");
            item.className = "source-item";

            item.textContent =
                `${source.document} | Page ${source.page}`;

            sourceBox.appendChild(item);
        });

        content.appendChild(sourceBox);
    }

    message.appendChild(avatar);
    message.appendChild(content);

    chatMessages.appendChild(message);

    message.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });
}

// Send question to FastAPI
async function askQuestion(question) {
    addMessage(question, "user");

    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        addMessage(
            data.answer || "No answer was returned.",
            "assistant",
            data.sources || []
        );

    } catch (error) {
        console.error("Error:", error);

        addMessage(
            "Unable to connect to the AI server. Please check whether the application is running and try again.",
            "assistant"
        );

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Ask AI";
        questionInput.focus();
    }
}

// Handle form submission
questionForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question || sendButton.disabled) {
        return;
    }

    questionInput.value = "";
    askQuestion(question);
});

// Handle suggested questions
document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;

        if (question && !sendButton.disabled) {
            askQuestion(question);
        }
    });
});

// Enter to submit, Shift + Enter for a new line
questionInput.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        questionForm.requestSubmit();
    }
});
