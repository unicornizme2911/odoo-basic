odoo.define('chat_module.chat', function (require) {
    'use strict';

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var QWeb = core.qweb;

    var ChatAction = AbstractAction.extend({
        template: 'chat_template',

        init: function (parent, context) {
            this._super(parent, context);
            this.currentConversationId = null;
            this.conversations = {
                1: {
                    id: 1,
                    name: 'John Doe',
                    messages: [
                        { id: 1, text: 'Hello! How are you?', sender: 'other', time: '10:30 AM' },
                        { id: 2, text: 'Hi John! I\'m doing well, thanks for asking.', sender: 'own', time: '10:32 AM' },
                        { id: 3, text: 'That\'s great to hear! Are you free for a meeting today?', sender: 'other', time: '10:33 AM' }
                    ]
                },
                2: {
                    id: 2,
                    name: 'Jane Smith',
                    messages: [
                        { id: 1, text: 'Hello, how are you?', sender: 'other', time: '09:15 AM' },
                        { id: 2, text: 'I\'m good, thanks! How about you?', sender: 'own', time: '09:20 AM' }
                    ]
                },
                3: {
                    id: 3,
                    name: 'Mike Johnson',
                    messages: [
                        { id: 1, text: 'Thanks for the update!', sender: 'other', time: '08:45 AM' },
                        { id: 2, text: 'You\'re welcome! Let me know if you need anything else.', sender: 'own', time: '08:50 AM' }
                    ]
                }
            };
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._bindEvents();
            });
        },

        _bindEvents: function () {
            var self = this;

            // Conversation selection
            this.$('.conversation-item').on('click', function () {
                var conversationId = parseInt($(this).data('conversation-id'));
                self._selectConversation(conversationId);
            });

            // Send message
            this.$('#send-button').on('click', function () {
                self._sendMessage();
            });

            // Enter key to send message
            this.$('#message-input').on('keypress', function (e) {
                if (e.which === 13) {
                    self._sendMessage();
                }
            });

            // Auto-resize message input
            this.$('#message-input').on('input', function () {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        },

        _selectConversation: function (conversationId) {
            var self = this;

            // Update active conversation
            this.$('.conversation-item').removeClass('active');
            this.$('.conversation-item[data-conversation-id="' + conversationId + '"]').addClass('active');

            this.currentConversationId = conversationId;
            var conversation = this.conversations[conversationId];

            // Update chat header
            this.$('#chat-username').text(conversation.name);
            this.$('#chat-status').text('Online');

            // Load messages
            this._loadMessages(conversationId);

            // Enable input
            this.$('#message-input').prop('disabled', false).focus();
            this.$('#send-button').prop('disabled', false);
        },

        _loadMessages: function (conversationId) {
            var conversation = this.conversations[conversationId];
            var $chatMessages = this.$('#chat-messages');

            $chatMessages.empty();

            if (conversation && conversation.messages) {
                conversation.messages.forEach(function (message) {
                    var messageHtml = this._createMessageHtml(message);
                    $chatMessages.append(messageHtml);
                }.bind(this));
            }

            // Scroll to bottom
            this._scrollToBottom();
        },

        _createMessageHtml: function (message) {
            var messageClass = message.sender === 'own' ? 'message own' : 'message other';
            var bubbleClass = message.sender === 'own' ? 'message-bubble own' : 'message-bubble other';

            return $(`
                <div class="${messageClass}">
                    <div class="${bubbleClass}">
                        <div class="message-text">${message.text}</div>
                        <div class="message-time">${message.time}</div>
                    </div>
                </div>
            `);
        },

        _sendMessage: function () {
            var self = this;
            var messageText = this.$('#message-input').val().trim();

            if (!messageText || !this.currentConversationId) {
                return;
            }

            var currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            // Add message to conversation
            var newMessage = {
                id: Date.now(),
                text: messageText,
                sender: 'own',
                time: currentTime
            };

            this.conversations[this.currentConversationId].messages.push(newMessage);

            // Add message to UI
            var messageHtml = this._createMessageHtml(newMessage);
            this.$('#chat-messages').append(messageHtml);

            // Clear input
            this.$('#message-input').val('');

            // Scroll to bottom
            this._scrollToBottom();

            // Show typing indicator and simulate response
            this._simulateResponse();
        },

        _simulateResponse: function () {
            var self = this;

            // Show typing indicator
            this.$('#typing-indicator').show();
            this._scrollToBottom();

            // Simulate response after 2-3 seconds
            setTimeout(function () {
                self.$('#typing-indicator').hide();

                var responses = [
                    "Thanks for your message!",
                    "I'll get back to you on that.",
                    "Sounds good to me!",
                    "Let me check and get back to you.",
                    "Perfect! Thanks for letting me know."
                ];

                var randomResponse = responses[Math.floor(Math.random() * responses.length)];
                var currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                var responseMessage = {
                    id: Date.now(),
                    text: randomResponse,
                    sender: 'other',
                    time: currentTime
                };

                self.conversations[self.currentConversationId].messages.push(responseMessage);

                var messageHtml = self._createMessageHtml(responseMessage);
                self.$('#chat-messages').append(messageHtml);

                self._scrollToBottom();
            }, Math.random() * 2000 + 1000); // Random delay between 1-3 seconds
        },

        _scrollToBottom: function () {
            var $chatMessages = this.$('#chat-messages');
            $chatMessages.scrollTop($chatMessages[0].scrollHeight);
        }
    });

    core.action_registry.add('chat_action', ChatAction);

    return ChatAction;
});
