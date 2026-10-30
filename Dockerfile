FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目
COPY . .

# 暴露端口（云托管默认走80）
EXPOSE 80

# 启动命令：注意把端口设为 80，并允许所有地址访问
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]