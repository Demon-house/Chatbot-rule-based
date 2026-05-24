from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------- RULE CHATBOT ----------------
def bot_reply(msg):
    msg = msg.lower()

    if "hello" in msg or "hi" in msg:
        return "Hello! How can I help you?"

    elif "how are you" in msg:
        return "I am fine, thank you!"

    elif "your name" in msg:
        return "I am a simple rule-based chatbot."

    elif "bye" in msg:
        return "Goodbye! Have a nice day."

    else:
        return "I didn't understand that..."

# ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ChatBot</title>

<style>
body {
    margin:0;
    font-family: system-ui;
    background: linear-gradient(135deg, #0f0f0f, #1a1a2e);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.container {
    width: 550px;
    height: 85vh;
    background: rgba(20,20,20,0.95);
    border-radius: 16px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
    box-shadow:0 0 30px rgba(0,0,0,0.5);
}

.header {
    padding:14px;
    text-align:center;
    font-weight:bold;
    color:white;
    background: rgba(255,255,255,0.05);
}

.chat {
    flex:1;
    padding:15px;
    overflow-y:auto;
    display:flex;
    flex-direction:column;
    gap:10px;
}

.msg {
    padding:12px;
    border-radius:12px;
    max-width:75%;
    font-size:14px;
}

.user {
    background:#2563eb;
    color:white;
    align-self:flex-end;
}

.bot {
    background:#2a2a2a;
    color:white;
    align-self:flex-start;
}

.input-box {
    display:flex;
    padding:12px;
    background: rgba(255,255,255,0.05);
}

input {
    flex:1;
    padding:12px;
    border:none;
    border-radius:10px;
    background:#111;
    color:white;
    outline:none;
}

button {
    margin-left:10px;
    padding:12px 16px;
    border:none;
    border-radius:10px;
    background:#3b82f6;
    color:white;
    cursor:pointer;
}

button:hover {
    background:#2563eb;
}
</style>

</head>

<body>

<div class="container">

<div class="header">Simple Rule ChatBot</div>

<div class="chat" id="chat"></div>

<div class="input-box">
<input id="msg" placeholder="Type message..." 
onkeydown="if(event.key==='Enter'){send()}">

<button onclick="send()">Send</button>
</div>

</div>

<script>

function addMsg(text, cls) {
    let div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;

    document.getElementById("chat").appendChild(div);

    document.getElementById("chat").scrollTop =
    document.getElementById("chat").scrollHeight;
}

async function send() {

    let input = document.getElementById("msg");
    let msg = input.value.trim();

    if (!msg) return;

    addMsg(msg, "user");

    input.value = "";

    let res = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: msg
        })
    });

    let data = await res.json();

    addMsg(data.reply, "bot");
}

</script>

</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    msg = data["message"]

    reply = bot_reply(msg)

    return jsonify({
        "reply": reply
    })

# ---------------- RUN ----------------
if __name__ == "__main__":

    print("Running at http://127.0.0.1:5055")

    app.run(
        host="0.0.0.0",
        port=5055,
        debug=False
    )