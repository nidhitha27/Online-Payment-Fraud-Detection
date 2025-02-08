// script.js
document.addEventListener("DOMContentLoaded", () => {
    const fraudForm = document.getElementById("fraudForm");
    const predictionResult = document.getElementById("predictionResult");
    const resultText = document.getElementById("resultText");

    fraudForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form from submitting to server for now

        // Get form data
        const type = document.getElementById("type").value;
        const amount = parseFloat(document.getElementById("amount").value);
        const oldBalance = parseFloat(document.getElementById("oldbalanceOrg").value);
        const newBalance = parseFloat(document.getElementById("newbalanceOrig").value);

        // Validate inputs
        if (!type || isNaN(amount) || isNaN(oldBalance) || isNaN(newBalance)) {
            alert("Please fill in all fields correctly!");
            return;
        }

        // Mock prediction logic
        let prediction = "Not Fraudulent"; // Default prediction
        if (amount > oldBalance || newBalance < 0) {
            prediction = "Fraudulent";
        }

        // Display prediction result
        resultText.textContent = prediction;
        predictionResult.style.display = "block"; // Make result visible
    });
});
