import os

HOST = "0.0.0.0"
PORT =  int(os.getenv("PORT", 8000)) 

# 智谱 API 配置
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/" 
ZHIPU_MODEL = "glm-4-flash-250414"

# 注意这里：优先去云端读 Key，本地读不到就用空字符串
ZHIPU_API_KEY =  os.getenv("ZHIPU_API_KEY", "")