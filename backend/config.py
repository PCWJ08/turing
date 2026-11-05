import os

HOST = "0.0.0.0"

# 云端会自动分配端口，本地默认用 8000
PORT = int(os.getenv("PORT", 8000))

# 智谱 API 配置
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 

ZHIPU_MODEL = "glm-4-flash-250414"

# 本地测试填入你的真实 Key；如果上传 GitHub，确保它是 os.getenv 格式，并删除真实Key
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")