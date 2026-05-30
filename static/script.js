function sendMsg(){

    let msg = document.getElementById("msg").value;

    if(!msg.trim()) return;

    let chatbox = document.getElementById("chatbox");

    let html = `

    <div class="message">

        <div class="user-box">

            <div class="user-msg">
                ${msg}
            </div>

        </div>

    </div>
    `;

    chatbox.innerHTML += html;

    fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:msg
        })

    })

    .then(res=>res.json())

    .then(data=>{

        data.reply.forEach(item=>{

            let bot = `

            <div class="message">

                <div class="bot-box">

                    <div class="bot-icon">
                        🤖
                    </div>

                    <div class="bot-msg">

                        <b>Q:</b> ${item.question}
                        <br><br>

                        <b>A:</b> ${item.answer}

                    </div>

                </div>

            </div>
            `;

            chatbox.innerHTML += bot;

            chatbox.scrollTop =
            chatbox.scrollHeight;

        });

    });

    document.getElementById("msg").value="";
}