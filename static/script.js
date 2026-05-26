function sendMsg(){

    let msg = document.getElementById("msg").value;
    if(!msg.trim()) return;

    let chatbox = document.getElementById("chatbox");

    chatbox.innerHTML += `<div class="user">${msg}</div>`;

    fetch("/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:msg})
    })
    .then(res=>res.json())
    .then(data=>{

        let parts = data.reply.split("\n\n");

        parts.forEach((p,i)=>{
            setTimeout(()=>{
                chatbox.innerHTML += `<div class="bot">${p}</div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
            }, i*300);
        });

    });

    document.getElementById("msg").value="";
}