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



## 安装部署

### 1. 环境要求

- Python 3.8 或更高版本
- Microsoft SQL Server 2019 或更高版本
- ODBC Driver for SQL Server

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库配置

复制配置文件模板：

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

编辑 `.streamlit/secrets.toml` 文件，填入真实的数据库连接信息：

```toml
[default]
db_host = "your_sql_server_host"
db_port = 1433
db_name = "your_database_name"
db_username = "your_username"
db_password = "your_password"
```

### 4. 运行应用

```bash
streamlit run main.py
```

应用将在 `http://localhost:8501` 启动。

## 使用说明

### 初始化数据库

首次运行时，请：
1. 点击侧边栏的"初始化数据库"按钮
2. 系统将自动创建所需的表结构
3. 初始化基础设备类型数据

### 主要功能

1. **批次查询**
   - 输入批次号查询详细信息
   - 查看最近的批次列表

2. **设备状态**
   - 查看所有设备的当前状态
   - 包括设备类型、当前产品、批次号等

3. **报表生成**
   - 选择设备和报表类型
   - 自动生成格式化的生产报表
   - 支持Excel导出（待实现）

4. **数据管理**
   - 批次数据管理
   - 设备信息管理
   - 系统状态监控

## 项目结构

```
Batch_Report_Generator/
├── main.py                    # 主应用程序
├── models.py                  # SQLAlchemy 数据模型
├── database.py                # 数据库连接和管理
├── report.py                  # 报表生成模块
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明
├── .streamlit/
│   ├── config.toml           # Streamlit 配置
│   └── secrets.toml.template # 数据库配置模板
└── ...
```

## 开发说明

### 数据模型

所有数据模型定义在 `models.py` 中，使用 SQLModel 实现：

- 类型安全的数据模型
- 自动生成数据库表结构
- 支持 Pydantic 数据验证

### 数据库连接

使用连接池管理数据库连接：

```python
from database import get_session

with get_session() as session:
    # 数据库操作
    pass
```

### 添加新设备类型

1. 在 SQL 中创建对应的实时表、归档表和报表表
2. 在 `models.py` 中添加对应的 SQLModel 类
3. 在 `database.py` 的 `init_device_types()` 中添加设备类型初始化
4. 在 `main.py` 中添加对应的报表生成逻辑

## 待实现功能

- [ ] 报表自定义功能
- [ ] 更多设备类型支持（单效、双效、醇沉等）
- [ ] 数据可视化图表
- [ ] 用户权限管理
- [ ] 批次数据的增删改功能
- [ ] 系统日志记录
- [ ] 数据备份和恢复

## 注意事项

1. 确保 SQL Server 服务正在运行
2. 检查防火墙设置，确保端口 1433 可访问
3. 数据库用户需要有相应的读写权限
4. 首次运行前需要初始化数据库结构

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

---

© 2025 批次报表生成器 - 基于 Streamlit + SQLAlchemy 构建
