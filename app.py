from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "API is working!"

@app.route("/chat", methods=["GET"])
def chat():
    user_input = request.args.get("message")
    if not user_input:
        return jsonify({"response": "Please provide a message"}), 400

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.debug = True  # enable debug mode
    port = int(os.environ.get("PORT", 8080))  # let render handle port
    app.run(host="0.0.0.0", port=port)
    
