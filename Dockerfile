FROM python:3.10-slim

WORKDIR /app

# 复制依赖并安装（加入清华源加速）
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制所有项目文件
COPY . .

# 暴露80端口
EXPOSE 80

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
