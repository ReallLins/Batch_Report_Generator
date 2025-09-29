# Batch_Report_Generator · Copilot 指南

## 项目速览
- Streamlit 单体应用，入口在 `app.py`，通过 `streamlit_option_menu` 驱动侧边栏选项。
- 页面模块置于 `app_pages/`，每个文件暴露 `page()`，由主程序按标题路由。
- 业务面向批次监控、批次查询和报表生成三大场景，均依赖 SQL Server 数据。

## 数据访问与配置
- `database_config.DatabaseConfig` 从 `st.secrets.db_conn` 拉取连接信息，使用 `@st.cache_resource` 复用实例；确保 `.streamlit/secrets.toml` 具备该节并不要提交真实凭据。
- 所有查询通过 `with database_config.get_session()` 获取 SQLAlchemy Session，再用 `pd.read_sql(..., session.connection())` 返回 DataFrame；新增查询保持这一惯例。
- 主要 ORM 定义集中在 `models.py`，其中 `ARCHIVE_TABLE_MAPPING` / `get_archive_table_class` 决定可报表的历史表。

## 报表数据流水
- 报表生成流程：`app_pages/report_generate.page()` → `get_data.get_report_data_df()` → `clean_data.DataCleanerFactory.clean_dataframe()` → `clean_data.ReportTemplateProcessor.convert_to_template_df()` → `report.get_report()` 输出 Excel（`openpyxl`）。
- `clean_data` 通过 dataclass（如 `TQReportData`）清洗字段，`ReportTemplateProcessor` 将其编排成 `sections`，渲染时再转回旧格式；扩展报表需同步更新 dataclass、工厂映射和模板处理器。
- Excel 样式集中在 `report.BaseReport`，列宽、字体、合并策略已封装，避免直接操作 `openpyxl`。

## Streamlit UI 约定
- 表格展示统一使用 `st_aggrid`，并在 `app_pages/*` 里复用同一套 JS 片段（`JS_ON_GRID_READY` 等）；若需新表格，优先从 `static_var.py` 引入现有常量以避免重复代码。
- 交互按钮/下载逻辑用 `@st.fragment` 包裹，减少 Streamlit 重跑；新增耗时操作时保持这一模式。
- 主题参数大量使用 `StAggridTheme(base='quartz').withParams(...)`，保持配色一致即可获得统一外观。

## 开发与运行
- 依赖列在 `requirements.txt`，项目当前使用 Python 3.13 语法（PEP 604 联合类型），请确保解释器 ≥3.10。
- 本地启动：`pip install -r requirements.txt` 后执行 `streamlit run app.py`。仓库内的 `start.sh/start.bat` 与 `DEPLOYMENT.md` 仍指向 `main.py`/`sqlmodel`，需要手动改为 `app.py` 后再用。
- 数据库为 SQL Server（通过 `pymssql`），远程连接前确认网络与凭据；无离线模式。

## 常见坑与排查
- `get_report_data_df` 假设 `T_Device_Type.archive_table_name` 可在 `ARCHIVE_TABLE_MAPPING` 中解析，否则会抛出 `ValueError`；添加新设备时别忘登记。
- 批次查询返回的时间列需通过 `clean_data.get_formatted_datetime_df` 统一为字符串，否则 AG-Grid 会在含 `NaT` 时崩溃。
- 仓库包含真实 `.streamlit/secrets.toml` 示例，clone 后请立即替换或将其加入 `.gitignore`，避免泄露。
- 文档仍提及 `database.py`、`test_system.py` 等旧文件；参考实际源文件（`database_config.py`, `get_data.py`）实现。

## 扩展提示
- 新增设备类型：补齐 SQL 表→在 `models.py` 中建 ORM → 更新 `ARCHIVE_TABLE_MAPPING`、`DataCleanerFactory.CLEANER_MAPPING`、`ReportGeneratorFactory.GENERATOR_MAPPING`，并扩展 `Report_Template/report_template.py` 与对应模板处理器。
- 若需要对接外部历史接口，参照 `his_database_api/` 的 JSON 定义设计数据字段，再在 `get_data` 中落地查询与拼装。
