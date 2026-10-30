import asyncio
import random
import time
import re
from openai import AsyncOpenAI

import config
from ws_manager import manager

client = AsyncOpenAI(
    base_url=config.ZHIPU_BASE_URL,
    api_key=config.ZHIPU_API_KEY
)

PERSONAS = {
    "晚风": "你是个感性杠精，喜欢从情感角度反驳别人，经常用反问句质疑对方，偶尔发点小脾气。",
    "阿水": "你是个暴躁老哥，受不了啰嗦，说话很冲，喜欢直接怼人，经常发牢骚。",
    "老K": "你是个高高在上的懂哥，觉得别人说的都没营养，喜欢用“就这？”、“别吹了”来冷嘲热讽。",
    "小橘": "你是个八卦精，喜欢大惊小怪，动不动就发“真的假的”、“啊？不会吧”，喜欢插嘴。"
}

chat_history = []
last_spoke_time = {name: 0 for name in PERSONAS}
last_activity_time = time.time()    # 最后一次有人说话的时间
last_human_time = time.time()       # 最后一次【真人】说话的时间
last_api_call_time = 0 

def add_history(sender, text):
    global last_activity_time
    chat_history.append(f"[{sender}]: {text}")
    if len(chat_history) > 8: 
        chat_history.pop(0)
    last_activity_time = time.time()

async def ai_speak(player_name, prompt_type="chat", human_msg=None):
    global last_api_call_time
    
    now = time.time()
    wait_time = 1.5 - (now - last_api_call_time)
    if wait_time > 0:
        await asyncio.sleep(wait_time)
    last_api_call_time = time.time()

    persona = PERSONAS[player_name]
    history_str = "\n".join(chat_history)
    
    base_rules = """
【群聊法则】
1. 像发微信一样，大部分时间只说极其简短的半句话（5-15字）。
2. 偶尔可以发一句长一点的话，但绝对不能超过30字！绝对不要长篇大论。
3. 你只是群里的网友，禁止模拟其他人，不准出现任何人的名字或冒号。
4. 说话要有攻击性或者嘲讽感，绝对不要顺着别人说好话。
5. 严禁 Emoji。"""
    
    if prompt_type == "reply_human":
        prompt = f"""你是网友“{player_name}”，性格：{persona}
群友“圆周率”说：“{human_msg}”
{base_rules}
请立刻针对他的话发表看法："""
    else:
        prompt = f"""你是网友“{player_name}”，性格：{persona}
群聊记录：
{history_str}
{base_rules}
请顺着记录开喷或反驳："""

    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=config.ZHIPU_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=40, 
                temperature=0.9
            ),
            timeout=15.0
        )
        text = response.choices[0].message.content.strip()
        
        text = text.split('\n')[0]
        if '：' in text: return
        for name in ["晚风", "阿水", "老K", "小橘", "圆周率"]:
            if name in text: return
            
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text).strip()

        if len(text) > 30 and random.random() < 0.7:
            return
                
        if text and len(text) >= 2: 
            last_spoke_time[player_name] = time.time()
            add_history(player_name, text)
            await manager.broadcast(f"{player_name}::{text}")
            
    except Exception as e:
        if "429" not in str(e):
            print(f"[{player_name}] 报错: {e}")

async def process_message(sender, content, is_human):
    global last_activity_time, last_human_time
    last_activity_time = time.time()
    last_human_time = time.time() # 只要真人说话，立刻刷新挂机时间
    
    if is_human:
        chat_history.clear()
        chat_history.append(f"[圆周率]: {content}")
        
        responders = random.sample(list(PERSONAS.keys()), 3)
        for ai in responders:
            asyncio.create_task(ai_speak(ai, prompt_type="reply_human", human_msg=content))
            
async def auto_chat_loop():
    global chat_history, last_activity_time, last_human_time
    while True:
        await asyncio.sleep(2)
        
        # 🛑 终极防烧 Token 第一层：网页全关了，直接休眠
        if len(manager.active_connections) == 0:
            continue
            
        now = time.time()
        idle_time = now - last_activity_time
        human_idle_time = now - last_human_time
        
        # 🛑 终极防烧 Token 第二层：网页虽然开着，但真人超过 5 分钟（300秒）没说话了，判定为挂机/发呆，AI 强制闭嘴！
        if human_idle_time > 300:
            if len(chat_history) > 0:
                print("💤 真人挂机超过5分钟，AI 停止自嗨，进入休眠。")
                chat_history.clear()
            continue
            
        # 正常情况：真人活跃中，只要冷场 4 秒，立刻开始自嗨
        if idle_time > 4:
            available = [n for n in PERSONAS if now - last_spoke_time[n] > 5]
            if available:
                next_ai = random.choice(available)
                asyncio.create_task(ai_speak(next_ai, prompt_type="chat"))
                last_activity_time = time.time()