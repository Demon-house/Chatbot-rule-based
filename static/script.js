function sendMsg(){

    let msg = document.getElementById("msg").value;

    if(!msg.trim()) return;

    let chatbox = document.getElementById("chatbox");

    // create user message element safely
    const messageEl = document.createElement('div');
    messageEl.className = 'message';

    const userBox = document.createElement('div');
    userBox.className = 'user-box';

    const userMsg = document.createElement('div');
    userMsg.className = 'user-msg';
    userMsg.textContent = msg; // safe insertion

    userBox.appendChild(userMsg);
    messageEl.appendChild(userBox);
    chatbox.appendChild(messageEl);

    fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:msg
        })

    })

    .then(res => res.json())
    .then(data => {
        if (!data || !Array.isArray(data.reply)) return;

        data.reply.forEach(item=>{
            const messageEl = document.createElement('div');
            messageEl.className = 'message';

            const botBox = document.createElement('div');
            botBox.className = 'bot-box';

            const botIcon = document.createElement('div');
            botIcon.className = 'bot-icon';
            botIcon.textContent = '🤖';

            const botMsg = document.createElement('div');
            botMsg.className = 'bot-msg';

            // build Q/A with safe text nodes and basic formatting
            const qLabel = document.createElement('b');
            qLabel.textContent = 'Q:';

            const qText = document.createElement('div');
            qText.textContent = item.question || '';
            qText.style.marginTop = '4px';

            const aLabel = document.createElement('b');
            aLabel.textContent = 'A:';

            const aText = document.createElement('div');
            aText.textContent = item.answer || '';
            aText.style.marginTop = '6px';

            botMsg.appendChild(qLabel);
            botMsg.appendChild(document.createElement('br'));
            botMsg.appendChild(document.createElement('br'));
            botMsg.appendChild(qText);
            botMsg.appendChild(document.createElement('br'));
            botMsg.appendChild(document.createElement('br'));
            botMsg.appendChild(aLabel);
            botMsg.appendChild(document.createElement('br'));
            botMsg.appendChild(aText);

            botBox.appendChild(botIcon);
            botBox.appendChild(botMsg);

            messageEl.appendChild(botBox);
            chatbox.appendChild(messageEl);

            chatbox.scrollTop = chatbox.scrollHeight;
        });
    })
    .catch(err => {
        console.error('Chat request failed', err);
    });

    document.getElementById("msg").value="";
}