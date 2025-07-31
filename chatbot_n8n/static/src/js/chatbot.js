let conversationId = window.conversationId !== 'false' ? window.conversationId : null;

document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    console.log(conversationId)
    function appendMessage(role, text) {
        const div = document.createElement('div');
        div.className = role === 'user' ? 'text-end' : 'text-start';
        div.innerHTML = `<div class="p-2 mb-2 rounded bg-${role === 'user' ? 'primary' : 'light'} text-${role === 'user' ? 'white' : 'dark'}">${text}</div>`;
        chatWindow.appendChild(div);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function sendMessage(){
        const text = input.value.trim();
        if (!text) return;

        appendMessage('user', text);
        input.value = '';
        appendMessage('bot', '⏳...');
        let data = {
            conversation_id: conversationId !== 'false' ? conversationId : null,
            content: text
        }
        fetch('/chatbot/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if (data.conversation_id) {
                conversationId = data.conversation_id;
            }
            chatWindow.lastChild.remove();
            const reply = data.result.reply || '🤖 Không có phản hồi từ bot';
            appendMessage('bot', reply);
        })
        .catch(() => appendMessage('bot', '❌ Lỗi kết nối đến máy chủ.'));
    }
    sendBtn.addEventListener('click', sendMessage);

    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
});
