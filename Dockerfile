FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
# 保持你原有的阿里云镜像源，加速下载
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . .

WORKDIR /app/backend

# Render 默认分配的端口通常是 10000
EXPOSE 10000

# 用 sh -c 解析环境变量，这样 Render 分配的 $PORT 就能生效
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]