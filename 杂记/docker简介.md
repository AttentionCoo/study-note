# Docker / Dockerfile / docker-compose 详解

---

## 1. Docker（容器引擎）

> 一句话：Docker 是一个轻量级虚拟机，把你的应用和它需要的所有环境打包成一个箱子，到哪都能跑。

**解决的问题**：

- 同事说：我电脑上能跑啊
- 服务器上缺 Python 3.10、缺 JDK 21、缺 MySQL 8.0
- 不同项目需要不同版本的同一个软件

Docker 让每个应用跑在隔离的容器里，自带所有依赖，互不干扰。

**LearnAgent 项目容器拓扑**：

+---------------------------------------------------------+
|                     Docker 引擎                          |
|  +----------+ +----------+ +--------------+            |
|  |  MySQL   | |  Redis   | |    Model     |            |
|  |  容器    | |  容器    | |    容器      |            |
|  |  :3306   | |  :6379   | |    :8000     |            |
|  +----------+ +----------+ +--------------+            |
|  +--------------+ +--------------+                      |
|  |   Backend    | |   Frontend   |                      |
|  |    容器      | |    容器      |                      |
|  |    :8080     | |    :5173     |                      |
|  +--------------+ +--------------+                      |
+---------------------------------------------------------+

---

## 2. Dockerfile（镜像配方）

> 一句话：Dockerfile 是菜谱，定义了怎么从零构建一个应用的镜像。

**类比**：Dockerfile 是菜谱 -> 镜像是做好的菜 -> 容器是正在吃的那盘。

### 2.1 Model — Python Dockerfile

FROM python:3.10-slim              # 基础镜像：Python 3.10 精简版
WORKDIR /app                       # 工作目录
COPY requirements.txt .            # 先复制依赖文件（利用缓存）
RUN pip install -r requirements.txt # 安装依赖
COPY . .                           # 复制源代码
CMD ["python", "app/main.py"]      # 启动命令

**为什么 COPY 分两步？** Docker 每一行都是一个层。requirements.txt 不常变，但代码经常变。分开写可以让 Docker 缓存依赖安装层，只重新构建代码层，加速构建。

### 2.2 Backend — Java Maven 多阶段构建

# 阶段 1：构建阶段（用 Maven + JDK 21 编译）
FROM maven:3.9-eclipse-temurin-21 AS build
COPY pom.xml .
RUN mvn dependency:go-offline        # 下载依赖（可缓存）
COPY src/ src/
RUN mvn package -DskipTests          # 编译打包

# 阶段 2：运行阶段（只需要 JRE）
FROM eclipse-temurin:21-jre
COPY --from=build /app/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]

**多阶段构建的精妙之处**：构建阶段用 Maven（带 JDK + 依赖），最终镜像只留 JRE + jar 包，体积从 ~600MB 降到 ~200MB。

### 2.3 Frontend — Vue + Nginx

# 阶段 1：Node 构建
FROM node:20-alpine AS build
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build                    # 产出 dist/

# 阶段 2：Nginx 提供静态服务
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

---

## 3. docker-compose.yml（多容器编排）

> 一句话：docker-compose 是指挥家，告诉 Docker 怎么同时启动和管理多个容器，以及它们之间的网络、依赖关系。

**为什么要 docker-compose？** 项目有 5 个服务，手动逐个启动非常繁琐。

docker-compose 一键搞定：

  docker compose up -d --build

### 关键设计解析

services:
  mysql:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql              # 1. 数据持久化
      - ./backend/server/learningo_agents.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
                                                # 2. 自动建表
    healthcheck:                                # 3. 健康检查
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-p${DB_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 10

  backend:
    depends_on:
      mysql:
        condition: service_healthy   # 4. 等 MySQL 健康后才启动
      model:
        condition: service_healthy   # 4. 等 Model 健康后才启动
      redis:
        condition: service_started

  frontend:
    ports:
      - "5173:80"      # 5. 端口映射：宿主机 5173 -> 容器内 80

| 设计点 | 作用 |
|--------|------|
| 1. volumes | 数据持久化——容器删了，MySQL 数据还在 |
| 2. initdb.d | 首次启动自动执行 SQL，建表 + 插入初始数据 |
| 3. healthcheck | 不光是启动了，而是能正常响应了才算就绪 |
| 4. depends_on | 保证启动顺序，避免 Backend 连不上数据库就崩溃 |
| 5. ports | 把容器端口暴露到宿主机，浏览器才能访问 |

---

## 4. 三者关系总结

Dockerfile                  docker-compose.yml
   |                              |
   | 定义怎么做镜像              | 定义怎么编排容器
   |                              |
   v                              v
 镜像 (image)  ------------>  容器 (container) x N
   |                              |
   | docker build                 | docker compose up
   |                              |
   v                              v
 静态的、分层的文件包           运行的、有网络的、有状态的服务

### 一键启动流程

docker compose up -d --build
  |
  +--> 构建 backend 镜像（Dockerfile -> Maven 编译 -> jar）
  +--> 构建 frontend 镜像（Dockerfile -> npm build -> nginx）
  +--> 构建 model 镜像（Dockerfile -> pip install -> uvicorn）
  +--> 拉取 mysql:8.0 镜像（公共镜像）
  +--> 拉取 redis:7-alpine 镜像（公共镜像）
  |
  +--> 按依赖顺序启动：
        mysql (健康) -> redis (启动) -> model (健康) -> backend -> frontend

### 常用命令

| 命令 | 作用 |
|------|------|
| docker compose up -d --build | 构建并后台启动所有服务 |
| docker compose down | 停止并删除所有容器 |
| docker compose down -v | 停止并删除容器 + 数据卷（警告：数据会丢失） |
| docker compose ps | 查看所有容器运行状态 |
| docker compose logs -f <服务名> | 实时查看某服务日志 |
| docker compose restart <服务名> | 重启某个服务 |
| docker compose build --no-cache | 强制重新构建（不使用缓存） |
