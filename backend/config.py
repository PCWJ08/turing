# --- 服务器配置 ---
HOST = "0.0.0.0"
PORT = 8000

# --- 智谱 API 配置 ---
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 
ZHIPU_MODEL = "glm-4-flash"

# 👇👇👇 把你的智谱 API KEY 粘贴在下面这行引号里 👇👇👇
ZHIPU_API_KEY = "0ea39df8f8014506ae273e0299d77614.uJBIG0y9Wg4Mw3V9" 

# --- AI发言节奏控制 ---
AI_SPEAK_INTERVAL_MIN = 2    # AI间隔最短几秒
AI_SPEAK_INTERVAL_MAX = 6    # AI间隔最长几秒
AI_COOLDOWN_SECONDS = 10     # 同一个AI说完话后必须等几秒才能再说

# --- 聊天室规则 ---
MAX_MESSAGE_LENGTH = 60