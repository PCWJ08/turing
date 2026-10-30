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
    "晚风": "感性，喜欢共情，常说'确实'、'谁懂啊'。",
    "阿水": "水群乐子人，喜欢发'草'、'笑死'，随性。",
    "老K": "直男老网民，说话直接，不废话。",
    "小橘": "活泼好奇，喜欢问'真的假的'、'然后呢'。"
}

chat_history = []
last_spoke_time = {name: 0 for name in PERSONAS}

def add_history(sender, text):
    chat_history.append(f"{sender}: {text}")
    if len(chat_history) > 8: 
        chat_history.pop(0)

async def ai_speak(player_name, prompt_type="chat", human_msg=None):
    await asyncio.sleep(random.uniform(0.3, 1.2))
    
    persona = PERSONAS[player_name]
    history_str = "\n".join(chat_history)
    
    base_rules = """
【最高指令】
1. 你只是群里的普通网友，不是编剧！绝对禁止模拟其他人说话。
2. 严禁输出“某某：xxx”这种格式，严禁包含任何冒号，只输出你一个人要发的话。
3. 字数简短（15-30字），像微信发消息一样。
4. 直接输出纯文字，严禁 Emoji。"""
    
    if prompt_type == "reply_human":
        prompt = f"""你是网友“{player_name}”，性格：{persona}
群友“圆周率”说：“{human_msg}”
{base_rules}
请直接回复圆周率，只输出你要说的内容："""
    else:
        prompt = f"""你是网友“{player_name}”，性格：{persona}
群聊记录：
{history_str}
{base_rules}
请顺着记录吐槽或接茬，只输出你要说的内容："""

    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=config.ZHIPU_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.85
                # 🌟 彻底删除了报错的 stop 参数
            ),
            timeout=10.0
        )
        text = response.choices[0].message.content.strip()
        
        # 🌟 用极其暴力的正则清洗，替代 stop 参数
        # 1. 截断换行，只取第一段
        text = text.split('\n')[0]
        # 2. 如果包含冒号，截断冒号后面的内容（防止念台词）
        if '：' in text: text = text.split('：')[0]
        if ':' in text: text = text.split(':')[0]
        # 3. 如果包含其他AI的名字，直接截断
        for other in ["晚风", "阿水", "老K", "小橘", "圆周率"]:
            if other in text:
                text = text.split(other)[0]
        # 4. 过滤括号和Emoji
        text = re.sub(r'[\【\(\[].*?[\】\)\]]', '', text)
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        text = text.strip()

        # 如果清洗后没字了，直接作废
        if not text or len(text) < 2: 
            return
            
        last_spoke_time[player_name] = time.time()
        add_history(player_name, text)
        await manager.broadcast(f"{player_name}::{text}")
            
    except Exception as e:
        print(f"[{player_name}] 报错: {e}")

async def process_message(sender, content, is_human):
    add_history(sender, content)
    if is_human:
        chat_history.clear()
        chat_history.append(f"{sender}: {content}")
        responders = random.sample(list(PERSONAS.keys()), 2)
        for ai in responders:
            asyncio.create_task(ai_speak(ai, prompt_type="reply_human", human_msg=content))
            
async def auto_chat_loop():
    """群聊永动机"""
    while True:
        await asyncio.sleep(random.uniform(3.0, 6.0))
        if len(chat_history) > 0:
            now = time.time()
            available = [n for n in PERSONAS if now - last_spoke_time[n] > 4]
            if available:
                next_ai = random.choice(available)
                asyncio.create_task(ai_speak(next_ai, prompt_type="chat"))