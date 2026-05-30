from flask import Flask, render_template, request, jsonify, abort
from model import Chatbot
from utils.security import clean_input
import re

app = Flask(__name__)
bot = Chatbot()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():


    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"reply": [{"question": "", "answer": "Invalid JSON payload."}]}), 400

    raw_msg = payload.get("message") if isinstance(payload, dict) else None

    if not raw_msg:
        return jsonify({"reply": [{"question": "", "answer": "Invalid request: no message provided."}]}), 400



   
    msg = clean_input(raw_msg)

    try:
        raw = re.split(r'[?.!]', msg)

        queries = []

        for r in raw:

            if " and " in r:
                queries.extend(r.split(" and "))

            elif "," in r:
                queries.extend(r.split(","))

            else:
                queries.append(r)

        queries = [q.strip() for q in queries if q.strip()]

        if len(queries) > 5:
            return jsonify({"reply": [{"question": "", "answer": "Only 5 questions allowed."}]})

        responses = []

        subject = None

        for q in queries:

            if "numpy" in q:
                subject = "numpy"

            elif "tensorflow" in q:
                subject = "tensorflow"

            elif "pandas" in q:
                subject = "pandas"

            elif "pytorch" in q:
                subject = "pytorch"

            if "install" in q and subject:
                q = f"how to install {subject}"

            ans = bot.get_response(q)

            responses.append({
                "question": q,
                "answer": ans
            })

        return jsonify({"reply": responses})
    except Exception as e:
        print("Unhandled error in /chat:", e)
        return jsonify({"reply": [{"question": "", "answer": "Internal server error."}]}), 500

if __name__ == "__main__":
    # bind to localhost and disable debug to avoid accidental public exposure
    app.run(host="127.0.0.1", debug=False, port=5002)