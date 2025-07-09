# 部署指南 (Deployment Guide)

## 📦 快速部署

### 方法一：使用启动脚本（推荐）

#### macOS/Linux 用户
```bash
# 1. 进入项目目录
cd /path/to/Batch_Report_Generator

# 2. 运行启动脚本
./start.sh
```

#### Windows 用户
```batch
# 1. 进入项目目录
cd C:\path\to\Batch_Report_Generator

# 2. 运行启动脚本
start.bat
```

### 方法二：手动部署

#### 1. 环境准备
```bash
# 确保Python 3.8+已安装
python --version

# 安装依赖
pip install -r requirements.txt
```

#### 2. 数据库配置
```bash
# 创建配置目录
mkdir -p .streamlit

# 复制并编辑配置文件
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

编辑 `.streamlit/secrets.toml`：
```toml
# SQL Server 数据库配置
db_host = "your-sql-server-host"
db_port = 1433
db_name = "your-database-name"
db_username = "your-username"
db_password = "your-password"
```

#### 3. 系统测试
```bash
# 运行系统测试
python test_system.py
```

#### 4. 启动应用
```bash
# 启动 Streamlit 应用
streamlit run main.py
```

## 🔧 生产环境部署

### Docker 部署

#### 1. 创建 Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    freetds-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "main.py", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
```

#### 2. 构建和运行
```bash
# 构建镜像
docker build -t batch-report-generator .

# 运行容器
docker run -p 8501:8501 \
  -e DB_HOST=your-sql-server-host \
  -e DB_PORT=1433 \
  -e DB_NAME=your-database-name \
  -e DB_USERNAME=your-username \
  -e DB_PASSWORD=your-password \
  batch-report-generator
```

### 云服务部署

#### Streamlit Cloud
1. 将项目推送到 GitHub
2. 登录 [Streamlit Cloud](https://share.streamlit.io/)
3. 连接GitHub仓库
4. 配置环境变量
5. 部署应用

#### 其他云平台
- **Heroku**: 支持Python应用部署
- **AWS ECS**: 容器化部署
- **Azure Container Instances**: 简单容器部署
- **Google Cloud Run**: 无服务器容器部署

## 📊 监控和维护

### 日志配置
```python
# 在 main.py 中添加日志配置
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控
- 使用 Streamlit 内置的性能监控
- 配置数据库连接池
- 监控内存使用情况

### 数据库维护
- 定期备份数据库
- 监控数据库连接数
- 优化查询性能

## 🔒 安全配置

### 数据库安全
- 使用最小权限原则
- 配置SSL连接
- 定期更换密码

### 应用安全
- 配置防火墙规则
- 使用HTTPS
- 限制访问IP

### 配置文件安全
```bash
# 设置配置文件权限
chmod 600 .streamlit/secrets.toml

# 不要将敏感信息提交到版本控制
echo ".streamlit/secrets.toml" >> .gitignore
```

## 🚨 故障排除

### 常见错误

#### 1. 数据库连接失败
```
解决方案：
- 检查数据库服务器状态
- 验证连接字符串
- 确认网络连通性
- 检查防火墙设置
```

#### 2. 端口占用
```bash
# 查找占用端口的进程
lsof -i :8501

# 杀死进程
kill -9 <PID>

# 或使用其他端口
streamlit run main.py --server.port 8502
```

#### 3. 内存不足
```
解决方案：
- 增加系统内存
- 优化数据查询
- 实施数据分页
- 使用缓存机制
```

### 调试模式
```bash
# 启用调试模式
streamlit run main.py --server.runOnSave true --server.enableCORS false --logger.level debug
```

## 📈 性能优化

### 缓存策略
- 使用 `@st.cache_data` 缓存数据
- 使用 `@st.cache_resource` 缓存资源
- 合理设置缓存过期时间

### 数据库优化
- 添加适当的索引
- 优化查询语句
- 使用连接池

### 前端优化
- 使用 `st.session_state` 管理状态
- 避免不必要的重新渲染
- 优化大数据集的显示

## 🔄 版本更新

### 更新步骤
1. 停止现有应用
2. 备份数据和配置
3. 更新代码
4. 运行测试
5. 重新启动应用

### 回滚准备
- 保留上一版本的备份
- 准备回滚脚本
- 测试回滚过程

---

📧 如有问题，请联系技术支持团队。
