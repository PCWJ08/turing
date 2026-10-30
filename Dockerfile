FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
# 用阿里云镜像加速，防止超时
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
COPY . .
EXPOSE 80
# 明确指定启动命令，听 80 端口
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]