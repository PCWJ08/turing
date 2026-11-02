import os

HOST = "0.0.0.0"
# 优先读取 Render 分配的端口，读不到就用 8000
PORT = int(os.getenv("PORT", 8000)) 

# 智谱 API 配置
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 
ZHIPU_MODEL = "glm-4-flash"

# 注意这里：优先去云端读 Key，本地读不到就用空字符串
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")

# AI节奏控制
AI_SPEAK_INTERVAL_MIN = 2    # AI最短多久说一句话
AI_SPEAK_INTERVAL_MAX = 4    # AI最长多久说一句话
AI_COOLDOWN_SECONDS = 6      # 同一个AI说完后，冷却多久才能再说
MAX_MESSAGE_LENGTH = 60      # 字数限制上限
