document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chatToggle');
    const chatContainer = document.getElementById('chatContainer');
    const closeChat = document.getElementById('closeChat');
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');

    // Toggle Chat visibility
    chatToggle.addEventListener('click', () => {
        chatContainer.style.display = 'flex';
        chatToggle.style.display = 'none';
    });

    closeChat.addEventListener('click', () => {
        chatContainer.style.display = 'none';
        chatToggle.style.display = 'flex';
    });

    // Handle Sending Messages
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to UI
        appendMessage('user', message);
        userInput.value = '';

        // Show typing indicator or state
        const loadingMsg = appendMessage('bot', 'Thinking...');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            
            // Remove loading message
            chatMessages.removeChild(loadingMsg);

            if (data.response) {
                appendMessage('bot', data.response);
            } else {
                appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            chatMessages.removeChild(loadingMsg);
            appendMessage('bot', 'Unable to connect to the assistant. Is the server running?');
        }
    };

    const appendMessage = (role, text) => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', `${role}-message`);
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msgDiv;
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
