import os

# --- 服务器配置 ---
HOST = "0.0.0.0"
PORT = 80

# --- 智谱 API 配置 ---
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 
ZHIPU_MODEL = "glm-4-flash"

# 🌟 关键修改：如果云端没读到环境变量，就用后面的备用 Key
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "0ea39df8f8014506ae273e0299d77614.uJBIG0y9Wg4Mw3V9")

# --- AI发言节奏控制 ---
AI_SPEAK_INTERVAL_MIN = 2
AI_SPEAK_INTERVAL_MAX = 6
AI_COOLDOWN_SECONDS = 10
MAX_MESSAGE_LENGTH = 60
