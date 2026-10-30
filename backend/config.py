import os

# --- 服务器配置 ---
HOST = "0.0.0.0"
PORT = 80

# --- 智谱 API 配置 ---
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 
ZHIPU_MODEL = "glm-4-flash"

# 🌟 关键：优先读取云端的 ZHIPU_API_KEY，如果没有，用后面的备用 key
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "你本地测试用的Key填这里")

# --- AI发言节奏控制 ---
AI_SPEAK_INTERVAL_MIN = 2
AI_SPEAK_INTERVAL_MAX = 6
AI_COOLDOWN_SECONDS = 10

# --- 聊天室规则 ---
MAX_MESSAGE_LENGTH = 60
