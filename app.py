from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# get openai api key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

@app.route("/")
def home():
    return "API is working!"

@app.route("/chatgpt", methods=["GET"])
def chatgpt():
    user_input = request.args.get("message")
    if not user_input:
        return jsonify({"response": "Please provide a message"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    
