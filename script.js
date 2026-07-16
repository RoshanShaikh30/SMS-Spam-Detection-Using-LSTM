async function detectSpam() {

    const message = document.getElementById("message").value;

    if (message.trim() === "") {
        alert("Please enter an SMS.");
        return;
    }

    const response = await fetch("/predict", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <h2>${data.prediction}</h2>
        <p>Confidence: ${data.confidence}%</p>
    `;
}