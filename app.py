from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# configure gemini api key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    return "API is working!"

@app.route("/chat", methods=["GET"], strict_slashes=False)
def chat():
    user_input = request.args.get("message")
    if not user_input:
        return jsonify({"response": "please provide a message"}), 400

    try:
        # use latest gemini model
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
