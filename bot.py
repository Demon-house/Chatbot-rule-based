from flask import Flask, render_template, request, jsonify
from model import Chatbot
import re

app = Flask(__name__)
bot = Chatbot()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json["message"].lower()

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
        return jsonify({"reply": "Max 5 questions allowed."})

    responses = []

    subject = None

    for q in queries:

        q_low = q.lower()

        if "numpy" in q_low:
            subject = "numpy"
        elif "pandas" in q_low:
            subject = "pandas"
        elif "tensorflow" in q_low:
            subject = "tensorflow"
        elif "pytorch" in q_low:
            subject = "pytorch"

        if "install" in q_low and subject:
            q = f"how to install {subject}"

        ans = bot.get_response(q)
        responses.append(f"Q: {q}\nA: {ans}")

    return jsonify({"reply": "\n\n".join(responses)})


if __name__ == "__main__":
   app.run(debug=True, port=5001)