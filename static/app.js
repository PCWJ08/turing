const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('send-btn');
const statusEl = document.getElementById('status');
const counterEl = document.getElementById('counter');
const meNameEl = document.getElementById('me-name');

// 默认名字，等后端发来真实序号后再更新
let myName = '圆周率';
meNameEl.textContent = myName;

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
    
    // 🌟 核心：拦截系统分配的专属名字
    if (text.startsWith("SYSTEM_INIT::")) {
        const parts = text.split("::");
        myName = parts[1];
        // 更新右上角的显示
        meNameEl.textContent = myName;
        return;
    }

    let sender = '', content = text;
    if (text.includes('::')) {
      const parts = text.split('::');
      sender = parts[0];
      content = parts.slice(1).join('::');
    }
    appendMessage(sender, content);
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
    // 只要名字以圆周率开头，全部高亮绿色
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

function send() {
  const val = inputEl.value.trim();
  if (!val) return;
  if (ws && ws.readyState === WebSocket.OPEN) {
    // 发送当前分配到的名字
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

connect();