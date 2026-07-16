from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import os

print("Loading model...")
model = load_model("spam_model.keras")
print("Model loaded!")

print("Loading tokenizer...")
tokenizer = joblib.load("tokenizer.pkl")
print("Tokenizer loaded!")

print("Flask starting...")

app = Flask(__name__)

# Load trained model
model = load_model("spam_model.keras")

# Load tokenizer
tokenizer = joblib.load("tokenizer.pkl")

MAX_LENGTH = 100


@app.route("/")
def home():
    return send_from_directory(".", "sms-frontend.html")   # Change if your HTML filename is different

@app.route("/bg.jpg")
def background():
    return send_from_directory(".", "bg.jpg")

@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def js():
    return send_from_directory(".", "script.js")


@app.route("/predict", methods=["POST"])
def predict():
    
    print("Predict endpoint hit!")

    data = request.get_json()
    
    print(data)

    sms = data["message"]

    sequence = tokenizer.texts_to_sequences([sms])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LENGTH,
        padding="post"
    )

    prediction = model.predict(padded, verbose=0)[0][0]
    
    print("Prediction:", prediction)
    print("Confidence:", round(float(prediction) * 100, 2))

    if prediction >= 0.5:
        result = "Spam"
        confidence = round(float(prediction) * 100, 2)
    else:
        result = "Ham"
        confidence = round((1 - float(prediction)) * 100, 2)

    return jsonify({
        "prediction": result,
        "confidence": confidence
    })
    
    


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)