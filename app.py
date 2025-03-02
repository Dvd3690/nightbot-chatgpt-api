from flask import Flask, request
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
    username = request.args.get("user", "user")  

    if not user_input:
        return "please provide a message", 400

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(
            f"Summarize this in 380 characters or less: {user_input}"
        )

        trimmed_response = response.text[:380] if response.text else "i couldn't generate a response."

        # remove \n and extra spaces
        cleaned_response = " ".join(trimmed_response.split())

        return f"{username}: {cleaned_response}"
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
