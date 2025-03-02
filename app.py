from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "API is working!"

@app.route("/chat", methods=["GET"])
def chat():
    user_input = request.args.get("message", "")
    if not user_input:
        return jsonify({"response": "Please provide a message"}), 400

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([user_input])

    return jsonify({"response": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  
    app.run(host="0.0.0.0", port=port)
    
