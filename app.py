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
            f"Summarize the following in **less than 380 characters**. Ensure the summary is **concise, meaningful, and does not cut off mid-sentence**: {user_input}"
        )

        # ensure the response is within 380 chars & ends at a full sentence
        full_response = response.text.strip()
        if len(full_response) > 380:
            sentences = full_response.split(". ")
            trimmed_response = ""
            for sentence in sentences:
                if len(trimmed_response) + len(sentence) + 2 <= 380:  # +2 for ". "
                    trimmed_response += sentence + ". "
                else:
                    break
            full_response = trimmed_response.strip()

        return f"{username}: {full_response}"
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
