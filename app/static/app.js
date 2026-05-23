let sessionId = null;
let isWaiting = false;

const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const loading = document.getElementById('loading');

function showLoading() {
    loading.style.display = 'flex';
    sendBtn.disabled = true;
    messageInput.disabled = true;
    isWaiting = true;
}

function hideLoading() {
    loading.style.display = 'none';
    sendBtn.disabled = false;
    messageInput.disabled = false;
    messageInput.focus();
    isWaiting = false;
}

function scrollToBottom() {
    chatArea.scrollTop = chatArea.scrollHeight;
}

function addMessage(role, content, intent) {
    // Remove welcome message if present
    const welcome = chatArea.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role}`;

    if (intent && role === 'assistant') {
        const tagLabels = { chat: '闲聊', health: '健康', emergency: '紧急' };
        const tag = document.createElement('span');
        tag.className = `intent-tag ${intent}`;
        tag.textContent = tagLabels[intent] || intent;
        bubble.appendChild(tag);
        bubble.appendChild(document.createElement('br'));
    }

    bubble.appendChild(document.createTextNode(content));
    chatArea.appendChild(bubble);
    scrollToBottom();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isWaiting) return;

    messageInput.value = '';
    addMessage('user', message);
    showLoading();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId }),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || '请求失败');
        }

        const data = await response.json();
        sessionId = data.session_id;
        addMessage('assistant', data.reply, data.intent);
    } catch (error) {
        addMessage('assistant', '抱歉，我暂时无法回复，请稍后再试。如果情况紧急，请拨打120或联系家人。');
    } finally {
        hideLoading();
    }
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendQuick(message) {
    messageInput.value = message;
    sendMessage();
}

function newChat() {
    sessionId = null;
    chatArea.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">🌸</div>
            <h2>您好！我是小龄</h2>
            <p>可以陪您聊聊天、说说心里话</p>
            <p>也可以问我健康方面的问题</p>
            <div class="quick-actions">
                <button onclick="sendQuick('今天天气真好，想出去走走')">☀️ 聊聊天气</button>
                <button onclick="sendQuick('高血压平时要注意什么？')">💊 健康知识</button>
                <button onclick="sendQuick('最近睡不太好，怎么办？')">😴 失眠调理</button>
                <button onclick="sendQuick('老年人每天运动多久合适？')">🚶 运动建议</button>
            </div>
        </div>
    `;
}

// Focus input on load
messageInput.focus();
