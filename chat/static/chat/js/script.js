function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

async function indexUrl() {
    const urlInput = document.getElementById('urlInput');
    const statusDiv = document.getElementById('statusMessage');
    const url = urlInput.value;

    if (!url) return;

    statusDiv.style.display = 'block';
    statusDiv.className = 'stAlert';
    statusDiv.style.backgroundColor = '#e0f2fe';
    statusDiv.innerHTML = '<div class="loader"></div> Indexing website content... This may take a moment.';

    try {
        const response = await fetch('/api/index/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.success) {
            statusDiv.style.backgroundColor = '#f0fdf4';
            statusDiv.style.color = '#166534';
            statusDiv.innerHTML = `✅ Successfully indexed! Found ${data.chunks_count} chunks.`;
        } else {
            statusDiv.style.backgroundColor = '#fef2f2';
            statusDiv.style.color = '#991b1b';
            statusDiv.innerHTML = `❌ Error: ${data.error}`;
        }
    } catch (e) {
        statusDiv.style.backgroundColor = '#fef2f2';
        statusDiv.style.color = '#991b1b';
        statusDiv.innerHTML = `❌ Error: ${e.message}`;
    }
}

function createTypingIndicator() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message assistant loading-message';
    msgDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    return msgDiv;
}

function appendMessage(role, content) {
    const messagesArea = document.getElementById('messagesArea');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;

    const avatar = role === 'user' ? '🧑‍💻' : '🤖';

    msgDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="content">${content}</div>
    `;

    messagesArea.appendChild(msgDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}


async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value;
    const messagesArea = document.getElementById('messagesArea');

    if (!message) return;

    appendMessage('user', message);
    chatInput.value = '';

    // Show typing generic/spinner
    const loadingMsg = createTypingIndicator();
    messagesArea.appendChild(loadingMsg);
    messagesArea.scrollTop = messagesArea.scrollHeight;

    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove loading message
        messagesArea.removeChild(loadingMsg);

        if (data.answer) {
            let content = data.answer;
            if (data.sources && data.sources.length > 0) {
                content += '<br><br><small><strong>Sources:</strong><ul>';
                data.sources.forEach(src => {
                    content += `<li><a href="${src.source}" target="_blank">${src.title || 'Source'}</a></li>`;
                });
                content += '</ul></small>';
            }
            appendMessage('assistant', content);
        } else {
            appendMessage('assistant', 'Sorry, I encountered an error.');
        }

    } catch (e) {
        messagesArea.removeChild(loadingMsg);
        appendMessage('assistant', `Error: ${e.message}`);
    }
}
