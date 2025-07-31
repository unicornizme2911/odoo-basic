document.addEventListener('DOMContentLoaded', function () {
    // Mock data for conversations
    const conversationsArray = window.conversations || [];
    const conversations = {};
    conversationsArray.forEach(c => {
        conversations[c.id] = c;
    });

    const newConversationBtn = document.getElementById('new-conversation-btn');
    if (newConversationBtn) {
        newConversationBtn.addEventListener('click', async function () {
            const conversationId = await createNewConversation();
            if (conversationId) {
                window.location.reload(); // Hoặc tự động thêm vào danh sách, rồi chọn luôn
            }
        });
    }

    let currentConversationId = null;

    // DOM elements
    const chatUsername = document.getElementById('chat-username');
    const chatStatus = document.getElementById('chat-status');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    const headerAvatar = document.getElementById('header-avatar');
    document.querySelector('#conversations-list').addEventListener('click', function (e) {
        const item = e.target.closest('.conversation-item');
        if (!item) return;

        const conversationId = item.dataset.conversationId;
        if (conversationId) {
            selectConversation(conversationId, item);
        }
    });

    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !sendButton.disabled) {
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    // Functions
    function selectConversation(conversationId, element) {
        // Remove active class from all items
        const allItems = document.querySelectorAll('.conversation-item');
        allItems.forEach(item => item.classList.remove('active'));

        // Add active class to selected item
        element.classList.add('active');

        // Update chat header
        const conversation = conversations[conversationId];
        chatUsername.textContent = conversation.name;
        chatStatus.textContent = conversation.status;
        // Update header avatar
        headerAvatar.className = `avatar ${conversation.avatar}`;

        // Load messages
        loadMessages(conversationId);

        // Enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();

        currentConversationId = conversationId;
    }

    function loadMessages(conversationId) {
        const conversation = conversations[conversationId];
        chatMessages.innerHTML = '';

        conversation.messages.forEach(message => {
            const messageElement = createMessageElement(message, conversation.avatar);
            chatMessages.appendChild(messageElement);
        });

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function createMessageElement(message, avatarClass) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.sent ? 'sent' : ''}`;

        const avatar = document.createElement('div');
        const bgClass = message.sent ? 'bg-primary' : 'bg-secondary';
        avatar.className = `avatar ${bgClass}`;
        avatar.innerHTML = '<i class="fas fa-user"></i>';

        const content = document.createElement('div');
        content.className = 'message-content';
        let html = '';
        if (message.image) {
            html += `<div style="margin-top: 8px;">
                <img src="data:image/png;base64,${message.image}" 
                    alt="Bot image" 
                    style="max-width: 200px; border-radius: 8px;" />
            </div>`;
        }

        html += `
            <div>${message.content}</div>
            <div class="message-time">${message.time}</div>
        `;
        content.innerHTML = html;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        return messageDiv;
    }

    async function sendMessage() {
        const messageText = messageInput.value.trim();
        if (!messageText) return;

        if (!currentConversationId || currentConversationId === 'false') {
            currentConversationId = await createNewConversation();
            if (!currentConversationId) return;
            await new Promise(resolve => setTimeout(resolve, 10));

            // // Tự động update giao diện chat
            // const conversation = conversations[currentConversationId];
            // chatUsername.textContent = conversation.name;
            // chatStatus.textContent = conversation.status;
            // headerAvatar.className = `avatar bg-secondary`;
            // chatMessages.innerHTML = '';
            //
            // // Hiển thị tin nhắn đầu tiên
            // const firstMessage = conversation.messages[0];
            // const firstMsgElement = createMessageElement(firstMessage, 'bg-primary');
            // chatMessages.appendChild(firstMsgElement);
        }
        const sendingConversation = currentConversationId;
        // Create new message
        const newMessage = {
            content: messageText,
            time: new Date().toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'}),
            sent: true
        };

        // Add to chat
        const messageElement = createMessageElement(newMessage, 'bg-primary');
        if (sendingConversation === currentConversationId){
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        if (!conversations[sendingConversation].messages) {
            conversations[sendingConversation].messages = [];
        }
        conversations[sendingConversation].messages.push(newMessage);

        // Clear input
        messageInput.value = '';
        messageInput.disabled = true;
        sendButton.disabled = true;

        showTypingIndicator();
        let data = {
            conversation_id: sendingConversation,
            content: messageText
        }
        fetch('/chatbot/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            hideTypingIndicator();
            const reply = data.result.reply || '🤖 Không có phản hồi từ bot';
            const imageBase64 = data.result.image_base64;
            const botMessage = {
                content: reply,
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                image: imageBase64
            };
            const botElement = createMessageElement(botMessage, 'bg-secondary')
            chatMessages.appendChild(botElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            conversations[sendingConversation].messages.push(botMessage);

            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        })
        .catch(err => {
            hideTypingIndicator();
            console.error('Gửi tin nhắn thất bại:', err);
            const errorMsg = {
                content: 'Lỗi gửi tin nhắn!',
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            chatMessages.appendChild(createMessageElement(errorMsg, 'bg-danger'));
            chatMessages.scrollTop = chatMessages.scrollHeight;

            messageInput.disabled = false;
            sendButton.disabled = false;
        });
    }

    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    async function createNewConversation() {
        try {
            const response = await fetch('/chatbot/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': odoo.csrf_token || ''
                },
                body: JSON.stringify({})
            });
            const data = await response.json();
            const newId = data.result.id;
            console.log('New conversation created with ID:', data.result);
            const newConversation = {
                id: newId,
                name: data.result.name || 'Cuộc trò chuyện mới',
                status: 'Đang hoạt động',
                avatar: 'bg-secondary',
                messages: []
            };
            conversations[newId] = newConversation;
            addConversationToList(newConversation);
            currentConversationId = newId;
            // Tự động chọn nó
            const newItem = document.querySelector(`[data-conversation-id="${newId}"]`);
            if (newItem) {
                selectConversation(newId, newItem);
            }
            return newId;
        } catch (error) {
            console.error('Lỗi khi tạo cuộc trò chuyện:', error);
            return null;
        }
    }

    function addConversationToList(conversation){
        const list = document.querySelector('#conversations-list ul');
        if (!list) return;

        const li = document.createElement('li');
        li.innerHTML = `
            <div class="conversation-item p-3" data-conversation-id="${conversation.id}">
                <div class="d-flex align-items-center">
                    <div class="position-relative me-3">
                        <div class="avatar ${conversation.avatar}">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="status-indicator bg-success"></div>
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mb-1 fw-semibold">${conversation.name}</h6>
                        <small class="text-muted d-block text-truncate">
                            ${conversation.messages[0]?.content || ''}
                        </small>
                        <small class="text-muted" style="font-size: 0.75rem;">
                            ${conversation.messages[0]?.time || ''}
                        </small>
                    </div>
                </div>
            </div>
        `;

        // Gắn sự kiện click
        const item = li.querySelector('.conversation-item');
        item.addEventListener('click', function () {
            selectConversation(conversation.id, item);
        });

        // Thêm vào đầu danh sách
        list.prepend(li);
    }
});
