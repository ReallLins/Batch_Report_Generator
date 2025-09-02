# 批次报表工具

## 系统概述

批次报表工具是一个基于Streamlit的Web应用，用于批次数据管理和报表生成。系统通过SQLAlchemy连接SQL Server数据库，提供设备监控、批次查询和报表生成功能。

### 技术栈

| 模块 | 技术 | 用途 |
|------|------|------|
| 前端界面 | Streamlit | Web UI框架 |
| 数据展示 | st-aggrid, streamlit-antd-components | 数据表格和组件 |
| 后端框架 | Python 3.13 | 核心开发语言 |
| ORM框架 | SQLAlchemy 2.0+ | 数据库访问 |
| 数据库 | SQL Server | 生产数据存储 |
| 数据处理 | Pandas | 数据分析处理 |
| 报表生成 | openpyxl | Excel文件生成 |
| 配置管理 | Streamlit Secrets | 敏感信息管理 |

## 系统架构图

### 整体架构

```mermaid
flowchart TB
    %% 外部用户和系统
    User[用户<br/>操作员/工程师]
    
    %% 核心系统
    BRG[批次报表工具<br/>Batch Report Generator]
    
    %% 外部系统
    HIS_API[历史数据库API<br/>HIS Database API]
    MSSQL[(SQL Server数据库<br/>生产数据存储)]
    TSDB[(时序数据库<br/>实时数据源)]
    
    %% 外部文件系统
    Templates[报表模板<br/>Excel Templates]
    Config[配置文件<br/>secrets.toml]
    
    %% 连接关系
    User -->|Web界面访问| BRG
    BRG -->|API调用| HIS_API
    BRG -->|数据库查询| MSSQL
    HIS_API -->|数据获取| TSDB
    BRG -->|读取模板| Templates
    BRG -->|读取配置| Config
    
    %% 输出
    BRG -->|设备监控| Machines[设备状态]
    BRG -->|批次查询| Batchs[批次状态]
    BRG -->|报表生成| Reports[Excel报表]
```

### 应用架构

```mermaid
flowchart TB
    %% 用户界面层
    subgraph "Web界面层"
        UI[Streamlit Web UI<br/>端口: 8501]
        Pages[页面模块<br/>device_state<br/>batch_query<br/>report_generate]
    end
    
    %% 应用层
    subgraph "应用服务层"
        App[主应用<br/>app.py]
        DataService[数据服务层<br/>get_data.py]
        ReportService[报表服务<br/>report.py]
        CleanService[数据清洗<br/>clean_data.py]
    end
    
    %% 数据访问层
    subgraph "数据访问层"
        DBConfig[数据库配置<br/>database_config.py]
        Models[数据模型<br/>models.py]
    end
    
    %% 外部系统
    subgraph "外部数据源"
        MSSQL[(SQL Server<br/>生产数据库)]
        HIS_API[历史数据API<br/>时序数据接口]
    end
    
    %% 文件系统
    subgraph "文件系统"
        Templates[Excel模板<br/>Report_Template/]
        Config[配置文件<br/>secrets.toml]
        Icons[图标资源<br/>icons/]
    end
    
    %% 连接关系
    UI --> App
    Pages --> DataService
    Pages --> ReportService
    App --> Pages
    
    DataService --> DBConfig
    DataService --> Models
    ReportService --> CleanService
    
    DBConfig --> MSSQL
    DataService --> HIS_API
    
    ReportService --> Templates
    DBConfig --> Config
    UI --> Icons
```

### 组件架构

```mermaid
flowchart TB
    %% 页面组件
    subgraph "页面组件 (app_pages/)"
        DS[设备状态页面<br/>device_state.py<br/>- 状态展示]
        BQ[批次查询页面<br/>batch_query.py<br/>- 批次查询<br/>- 实时/历史]
        RG[报表生成页面<br/>report_generate.py<br/>- 报表生成<br/>- 报表预览<br/>-Excel导出]
    end
    
    %% 核心组件
    subgraph "核心组件"
        GetData[数据获取模块<br/>get_data.py<br/>- 设备数据<br/>- 批次数据<br/>- 报表数据]
        CleanData[数据处理模块<br/>clean_data.py<br/>- 数据格式化<br/>- 数据转换]
        ReportGen[报表生成模块<br/>report.py<br/>- 样式配置<br/>- Excel生成]
    end
    
    %% 数据访问组件
    subgraph "数据访问组件"
        DBConf[数据库配置<br/>database_config.py<br/>- 连接管理<br/>- 会话管理]
        ModelsComp[数据模型<br/>models.py<br/>- ORM映射<br/>- 表结构定义]
    end
    
    %% 外部接口
    subgraph "外部接口"
        HISAPI[HIS API接口<br/>his_database_api/<br/>- 时序数据<br/>- 最值查询]
        Database[(数据库<br/>SQL Server<br/>- 设备表<br/>- 批次表<br/>- 归档表)]
    end
    
    %% 连接关系
    DS --> GetData
    BQ --> GetData
    RG --> GetData
    RG --> ReportGen
    
    GetData --> CleanData
    ReportGen --> CleanData
    
    GetData --> DBConf
    GetData --> ModelsComp
    
    DBConf --> Database
    GetData --> HISAPI
```

## 数据流程图

### 主要业务流程

```mermaid
flowchart TD
    Start([用户访问系统]) --> Login{系统初始化}
    Login -->Menu[主菜单选择]
    
    Menu --> Device[设备状态监控]
    Menu --> Query[批次查询]
    Menu --> Report[报表生成]
    
    %% 设备状态流程
    Device --> GetDevices[获取设备列表]
    GetDevices --> ShowStatus[展示设备状态]
    
    %% 批次查询流程
    Query --> QueryForm[查询条件设置]
    QueryForm --> SearchBatch[搜索批次数据]
    SearchBatch --> ShowBatch[展示批次列表]
    ShowBatch --> BatchDetail[查看批次详情]
    
    %% 报表生成流程
    Report --> SelectDevice[选择设备类型]
    SelectDevice --> SelectBatch[选择批次]
    SelectBatch --> PreviewReport[预览报表内容]
    PreviewReport --> GenerateReport[生成Excel报表]
    GenerateReport --> DownloadReport[下载报表文件]
```

### 数据处理流程

```mermaid
flowchart TD
    %% 数据源
    subgraph "数据源"
        DB[(SQL Server<br/>生产数据库)]
        HIS[HIS API<br/>历史数据接口]
    end
    
    %% 数据获取
    subgraph "数据获取层"
        GetRaw[原始数据获取<br/>get_data.py]
        GetHIS[历史数据获取<br/>HIS API调用]
    end
    
    %% 数据处理
    subgraph "数据处理层"
        Clean[数据清洗<br/>clean_data.py]
        Format[格式化处理]
        Validate[数据验证]
    end
    
    %% 业务逻辑
    subgraph "业务逻辑层"
        DeviceLogic[设备状态逻辑]
        BatchLogic[批次查询逻辑]
        ReportLogic[报表生成逻辑]
    end
    
    %% 输出层
    subgraph "输出层"
        WebUI[Web界面展示]
        ExcelReport[Excel报表]
        APIResponse[API响应]
    end
    
    %% 数据流向
    DB --> GetRaw
    HIS --> GetHIS
    
    GetRaw --> Clean
    GetHIS --> Clean
    
    Clean --> Format
    Format --> Validate
    
    Validate --> DeviceLogic
    Validate --> BatchLogic
    Validate --> ReportLogic
    
    DeviceLogic --> WebUI
    BatchLogic --> WebUI
    ReportLogic --> ExcelReport
    
    WebUI --> APIResponse
```

## 部署架构

```mermaid
flowchart LR
    %% 开发环境
    subgraph "开发环境"
        Dev[本地开发<br/>conda环境]
    end
    
    %% 生产环境
    subgraph "生产环境"
        App[应用服务器<br/>Streamlit App]
        DB[(数据库服务器<br/>SQL Server)]
        HIS[(历史数据服务<br/>HIS API Server)]
    end
    
    %% 网络连接
    Dev -->|部署| App
    App -->|数据库连接| DB
    App -->|API调用| HIS
    
    %% 用户访问
    Users[用户] -->|HTTP:8501| App
```

## 扩展预留

<!-- ### 功能扩展点

1. **认证授权模块**: 用户登录和权限管理
2. **数据缓存层**: Redis缓存提升性能
3. **任务调度器**: 定时报表生成
4. **消息通知**: 邮件/微信通知功能
5. **数据可视化**: 图表分析功能
6. **移动端适配**: 响应式设计优化

### 技术架构扩展

```mermaid
flowchart TB
    %% 当前架构 - 实线
    Current[当前单体架构<br/>Streamlit + SQLAlchemy]
    
    %% 扩展架构 - 虚线
    Future1[微服务架构<br/>API Gateway + Services]
    Future2[消息队列<br/>Redis/RabbitMQ]
    Future3[容器化部署<br/>Docker + K8s]
    Future4[监控告警<br/>Prometheus + Grafana]
    
    Current -.->|扩展| Future1
    Current -.->|扩展| Future2
    Current -.->|扩展| Future3
    Current -.->|扩展| Future4
    
    style Future1 stroke-dasharray: 5 5
    style Future2 stroke-dasharray: 5 5
    style Future3 stroke-dasharray: 5 5
    style Future4 stroke-dasharray: 5 5
``` -->
