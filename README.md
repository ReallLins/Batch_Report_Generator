# 批次报表生成器 (Batch Report Generator)

基于 Streamlit + SQLAlchemy 构建的批次报表生成系统，用于中药提取车间的DCS数据管理和报表生成。

## 🎯 系统特色

- **📊 统一数据源**: 所有报表数据按设备类型存放在 `T_XX_Batch_Archive` 归档表
- **🏭 设备监控**: 实时监控设备运行状态和批次进度
- **🔍 精确查询**: 支持按设备ID和批次号精确查询历史批次数据
- **📥 Excel导出**: 自动生成格式化的Excel报表，支持一键下载

## 功能特性

- 🔍 **批次查询**: 支持按批次号查询生产数据和历史批次列表
- 🏭 **设备状态**: 实时监控设备运行状态
- 📈 **报表生成**: 通过设备ID和批次号动态生成提取罐生产报表
- 🗃️ **数据管理**: 批次和设备数据的管理功能
- 📊 **可视化界面**: 基于 Streamlit 的现代化 Web 界面

## 技术栈

- **后端**: Python 3.13.5
- **Web框架**: Streamlit
- **ORM**: SQLAlchemy
- **数据库**: Microsoft SQL Server
- **数据处理**: Pandas
- **Excel处理**: openpyxl

## 数据库结构

系统包含以下主要表：

- `T_Device_Type`: 设备类型表
- `T_Device_Info`: 设备信息表
- `T_Batch`: 批次主表
- `T_Device_Batch`: 设备批次关联表
- `T_XX_Batch_Realtime`: 设备批次数据实时表
- `T_XX_Batch_Archive`: 设备批次数据归档表（**主要报表数据源**）

### 🔄 数据流程

1. **数据采集**: 实时数据写入 `T_TQ_Batch_Realtime` 表
2. **数据归档**: 批次完成后数据归档到 `T_TQ_Batch_Archive` 表
3. **报表生成**: 根据设备ID和批次号从设备批次关联表查询关联ID，从归档表动态查询数据生成报表

## 快速开始

### 1. 环境配置

```bash
# 克隆项目
git clone <repository-url>
cd Batch_Report_Generator

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

创建 `.streamlit/secrets.toml` 文件：

```toml
# 数据库配置
db_host = "your-sql-server-host"
db_port = 1433
db_name = "your-database-name"
db_username = "your-username"
db_password = "your-password"
```

### 3. 运行测试

```bash
# 运行系统测试
python test_system.py
```

### 4. 启动应用

```bash
# 启动 Streamlit 应用
streamlit run main.py
```

## 📋 使用指南

### 批次查询
- 输入批次号查询详细信息
- 查看最近的批次列表

### 设备状态
- 实时查看所有设备的运行状态
- 查看设备类型、当前产品和批次信息

### 报表生成
1. 输入**设备ID**（必填）
2. 输入**批次号**（必填）
3. 选择报表类型（目前支持提取罐报表）
4. 点击"生成报表"按钮
5. 查看报表详情并支持Excel导出

## 🔧 系统架构

```
用户界面 (Streamlit)
    ↓
业务逻辑 (app.py)
    ↓
数据模型 (models.py) ← → 数据库访问 (database.py)
    ↓
报表生成 (report.py)
    ↓
Excel文件输出
```

## 📈 报表内容

提取罐报表包含以下内容：

1. **基本信息**
   - 产品名称、批次号、设备信息、生成时间

2. **工艺参数**
   - 升温/保温设定温度和压力
   - 溶媒设定量

3. **生产过程**
   - 升温/保温阶段的时间记录
   - 压力变化范围

4. **生产结果**
   - 实际溶媒量和出液量
   - 保温温度范围

## 🛠️ 开发说明

### 关键设计变更

- **取消 T_TQ_Batch_Report 表**: 所有报表数据均从 `T_TQ_Batch_Archive` 表动态查询
- **手动输入批次号**: 用户需要手动输入批次号来生成报表，提供更灵活的查询方式
- **类型安全**: 使用 Protocol 定义报表数据接口，确保类型安全

### 添加新设备类型

1. 在 `models.py` 中添加新的设备归档表
2. 在 `report.py` 中添加对应的报表生成器
3. 在 `main.py` 中添加设备类型选择逻辑

## 🔍 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 `secrets.toml` 配置
   - 确认数据库服务正在运行

2. **报表生成失败**
   - 确认设备ID和批次号存在
   - 检查归档表中是否有对应数据

3. **Excel导出错误**
   - 检查 openpyxl 库是否正确安装
   - 确认报表数据完整性

### 测试命令

```bash
# 运行系统测试
python test_system.py

# 检查依赖
pip list | grep -E "(streamlit|sqlmodel|openpyxl|pandas)"
```

## 📄 许可证

[MIT License](LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

© 2025 批次报表生成器 - 基于 Streamlit + SQLAlchemy 构建