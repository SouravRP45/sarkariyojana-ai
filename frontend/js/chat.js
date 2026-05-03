let ws = null;
let isTyping = false;

function toggleChat(forceOpen = false) {
    const panel = document.getElementById('chat-panel');
    if (forceOpen === true || !panel.classList.contains('open')) {
        panel.classList.add('open');
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            connectWebSocket();
        }
    } else {
        panel.classList.remove('open');
    }
}

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Use window.location.host for production, fallback to localhost for dev if file://
    const host = window.location.host || 'localhost:8000';
    const wsUrl = `${protocol}//${host}/api/chat/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('Chat connected');
        // Initial greeting
        if (document.getElementById('chat-messages').children.length === 0) {
             appendMessage('bot', 'Hello! I am SarkariYojana AI. How can I help you with government schemes today?');
        }
    };
    
    ws.onmessage = (event) => {
        removeTypingIndicator();
        try {
            const data = JSON.parse(event.data);
            if (data.error) {
                appendMessage('bot', 'Sorry, ' + data.error);
            } else {
                appendMessage('bot', data.content);
            }
        } catch(e) {
            appendMessage('bot', 'An error occurred.');
        }
    };
    
    ws.onclose = () => {
        console.log('Chat disconnected. Will reconnect on next message.');
    };
}

function initChat() {
    document.getElementById('btn-send').addEventListener('click', sendMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Quick question pills
    document.querySelectorAll('.quick-q').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('chat-input').value = btn.textContent;
            sendMessage();
        });
    });
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    appendMessage('user', message);
    input.value = '';
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        connectWebSocket();
        // Wait briefly for connection
        setTimeout(() => sendToWs(message), 500);
    } else {
        sendToWs(message);
    }
}

function sendToWs(message) {
    showTypingIndicator();
    const payload = {
        message: message,
        user_profile: window.appState.userProfile
    };
    ws.send(JSON.stringify(payload));
}

function appendMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg-bubble msg-${role}`;
    
    // Simple markdown to HTML conversion for bold and links
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color:var(--primary);">$1</a>')
        .replace(/\n/g, '<br>');
        
    msgDiv.innerHTML = formattedText;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    if (isTyping) return;
    isTyping = true;
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.className = 'msg-bubble msg-bot';
    div.innerHTML = '<i>Typing...</i>';
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    isTyping = false;
    const ind = document.getElementById('typing-indicator');
    if (ind) ind.remove();
}
