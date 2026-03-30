// 🔹 TEXT SUMMARIZATION
async function summarizeText() {
    const text = document.getElementById("inputText").value;

    document.getElementById("output").innerText = "Processing...";

    const response = await fetch("https://ai-study-assistant.onrender.com/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();

    document.getElementById("output").innerText = data.result;
}


// 🔹 PDF UPLOAD
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");

    // check if file selected
    if (!fileInput.files[0]) {
        alert("Please select a PDF file first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById("output").innerText = "Processing PDF...";

    const response = await fetch("https://ai-study-assistant.onrender.com/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("output").innerText = data.result;
}