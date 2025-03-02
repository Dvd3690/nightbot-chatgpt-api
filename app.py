from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# configure latest gemini api key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    return "API is working!"

@app.route("/chat", methods=["GET"], strict_slashes=False)
def chat():
    user_input = request.args.get("message")
    username = request.args.get("user", "user")  

    if not user_input:
        return "please provide a message", 400

    try:
        # use latest gemini-1.5-flash (free & updated)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Summarize this in less than 380 characters, keeping full sentences: {user_input}"
        )

        cleaned_response = " ".join(response.text.split()) if response.text else "i couldn't generate a response."

        return f"{username}: {cleaned_response}"
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
