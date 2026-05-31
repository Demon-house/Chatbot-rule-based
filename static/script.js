document.addEventListener('DOMContentLoaded', ()=>{
    const textarea = document.getElementById('msg');
    const sendBtn = document.getElementById('sendBtn') || document.getElementById('send');
    const chatbox = document.getElementById('chatbox');
    const typing = document.getElementById('typingIndicator');

    function fmtTime(){
        const d = new Date();
        return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    }

    function showTyping(v){ if(!typing) return; typing.style.display = v? 'inline-block':'none'; }

    function appendUser(text){
        const el = document.createElement('div'); el.className='message';
        const bubble = document.createElement('div'); bubble.className='user-msg'; bubble.textContent = text;
        el.appendChild(bubble);
        chatbox.appendChild(el);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function appendBot(item){
        const el = document.createElement('div'); el.className='message';
        const icon = document.createElement('div'); icon.className='bot-icon'; icon.textContent='🤖';
        const bubble = document.createElement('div'); bubble.className='bot-msg';
        // assistant-only answer
        let answer='';
        if(typeof item==='string') answer=item;
        else if(item && (item.answer || item.text)) answer = item.answer||item.text;
        else answer = (item && item.toString) ? String(item) : '';
        bubble.textContent = answer;
        el.appendChild(icon); el.appendChild(bubble);
        chatbox.appendChild(el);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function sendMsg(){
        const msg = textarea.value||''; if(!msg.trim()) return;
        appendUser(msg); textarea.value=''; textarea.focus(); showTyping(true);
        fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
            .then(r=>r.json())
            .then(data=>{ showTyping(false); if(!data || !Array.isArray(data.reply)) return; data.reply.forEach(i=>appendBot(i)); })
            .catch(err=>{ showTyping(false); console.error(err); appendBot('There was an error contacting the assistant.'); });
    }

    textarea.addEventListener('keydown', e=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMsg(); } });
    if(sendBtn) sendBtn.addEventListener('click', sendMsg);
    window.sendMsg = sendMsg;
});