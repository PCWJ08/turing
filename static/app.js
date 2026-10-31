const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('send-btn');
const statusEl = document.getElementById('status');
const counterEl = document.getElementById('counter');
const meNameEl = document.getElementById('me-name');

// 🌟 改动：直接修改输入框提示词
inputEl.placeholder = "院长，请说点什么...";

// 🌟 改动：名字锁定机制
let savedName = localStorage.getItem("my_chat_name");
let myName = savedName || '圆周率';
if (savedName) meNameEl.textContent = savedName;

let ws = null;
let hasMessage = false;

function connect() {
  const proto = location.protocol === 'https:' ? 'wss://' : 'ws://';
  ws = new WebSocket(proto + location.host + '/ws/chat');

  ws.onopen = () => {
    statusEl.textContent = '已连接';
    sendBtn.disabled = false;
  };

  ws.onmessage = (event) => {
    const text = event.data;
    
    if (text.startsWith("SYSTEM_INIT::")) {
        if (!savedName) {
            const parts = text.split("::");
            myName = parts[1];
            localStorage.setItem("my_chat_name", myName);
            meNameEl.textContent = myName;
        }
        return;
    }

    let sender = '', content = text;
    if (text.includes('::')) {
      const parts = text.split('::');
      sender = parts[0];
      content = parts.slice(1).join('::');
    }
    
    appendMessage(sender, content);
    saveToLocal(sender, content); 
  };

  ws.onclose = () => {
    statusEl.textContent = '断开，重连中...';
    sendBtn.disabled = true;
    setTimeout(connect, 2000);
  };
}

function appendMessage(sender, content) {
  if (!hasMessage) {
    messagesEl.innerHTML = '';
    hasMessage = true;
  }
  const wrap = document.createElement('div');
  wrap.className = 'msg';
  
  if (sender) {
    const s = document.createElement('span');
    s.className = 'sender';
    s.textContent = sender;
    if (sender.startsWith('圆周率')) s.style.color = '#00ffaa';
    wrap.appendChild(s);
  }
  
  const c = document.createElement('span');
  c.className = 'content';
  c.textContent = content;
  if (sender.startsWith('圆周率')) c.style.color = '#00ffaa';
  
  wrap.appendChild(c);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// 🌟 改动：本地存档与读取
function saveToLocal(sender, content) {
    let history = JSON.parse(localStorage.getItem("chat_history") || "[]");
    history.push({ sender, content, time: Date.now() });
    if (history.length > 60) history.shift(); 
    localStorage.setItem("chat_history", JSON.stringify(history));
}

function loadHistory() {
    let history = JSON.parse(localStorage.getItem("chat_history") || "[]");
    const now = Date.now();
    history = history.filter(msg => now - msg.time < 2 * 60 * 60 * 1000);
    
    if (history.length > 0) {
        messagesEl.innerHTML = '';
        hasMessage = true;
        history.forEach(msg => {
            appendMessage(msg.sender, msg.content);
        });
    } else {
        const sysWrap = document.createElement('div');
        sysWrap.className = 'msg';
        sysWrap.innerHTML = `<span class="sender" style="color: #666;">[系统]</span><span class="content" style="color: #888;">警告：你已进入重度精神科，请尝试与患者交流...</span>`;
        messagesEl.innerHTML = '';
        messagesEl.appendChild(sysWrap);
        hasMessage = true;
    }
}

function send() {
  const val = inputEl.value.trim();
  if (!val) return;
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(myName + '::' + val);
    inputEl.value = '';
    updateCounter();
    inputEl.focus();
  }
}

function updateCounter() {
  counterEl.textContent = inputEl.value.length + ' / 60';
}

sendBtn.addEventListener('click', send);
inputEl.addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });
inputEl.addEventListener('input', updateCounter);

loadHistory();
connect();
