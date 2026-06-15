const API_URL = "https://ai-study-assistant-zjb3.onrender.com";

async function summarizeText() {
    const text = document.getElementById("inputText").value;
    const result = document.getElementById("result");

    if (!text.trim()) {
        result.innerText = "Please enter some text.";
        return;
    }

    result.innerText = "⏳ Generating AI summary...";

    try {
        const response = await fetch(`${API_URL}/summarize`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();
        result.innerText = data.result;

    } catch (error) {
        result.innerText = "❌ Error connecting to server.";
    }
}

async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const result = document.getElementById("result");

    if (!fileInput.files.length) {
        result.innerText = "Please choose a file.";
        return;
    }

    result.innerText = "⏳ Processing file...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        result.innerText = data.result;

    } catch (error) {
        result.innerText = "❌ Error uploading file.";
    }
}

function copySummary() {
    const text = document.getElementById("result").innerText;

    navigator.clipboard.writeText(text)
        .then(() => {
            alert("Summary copied successfully!");
        })
        .catch(() => {
            alert("Failed to copy summary.");
        });
}

function downloadPDF() {

    const summaryText =
        document.getElementById("result").innerText;

    if (
        !summaryText ||
        summaryText ===
        "Your AI-generated summary will appear here..."
    ) {
        alert("Generate a summary first.");
        return;
    }

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    const lines =
        doc.splitTextToSize(summaryText, 180);

    doc.setFontSize(14);

    doc.text(
        "AI Study Assistant Summary",
        10,
        10
    );

    doc.setFontSize(11);

    doc.text(
        lines,
        10,
        25
    );

    doc.save("AI_Study_Summary.pdf");
}