FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .

# 使用阿里云镜像源，避免 403 报错
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . .

EXPOSE 80

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
