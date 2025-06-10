# 使用 Python 轻量级镜像
FROM python:3.11.5-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 设置容器内的工作目录
WORKDIR /app

# 复制代码到容器中
COPY . /app

# 安装系统依赖
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*

# 安装 Python 项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认运行端口
EXPOSE 5000

# 运行 Flask
CMD ["flask", "run", "--host=0.0.0.0"]
