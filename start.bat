@echo off
chcp 65001 > nul
cls

echo 🚀 批次报表生成器启动脚本
echo ================================

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未找到，请先安装Python
    pause
    exit /b 1
)

REM 检查是否在正确的目录
if not exist "main.py" (
    echo ❌ 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查依赖
echo 🔍 检查依赖...
python -c "import streamlit, sqlmodel, openpyxl, pandas" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  缺少依赖，正在安装...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查配置文件
if not exist ".streamlit\secrets.toml" (
    echo ⚠️  数据库配置文件不存在
    echo 请创建 .streamlit\secrets.toml 文件并配置数据库连接信息
    echo 参考模板: .streamlit\secrets.toml.template
    
    set /p create_config=是否要创建配置文件模板？ (y/n): 
    if /i "%create_config%"=="y" (
        if not exist ".streamlit" mkdir .streamlit
        if exist ".streamlit\secrets.toml.template" (
            copy ".streamlit\secrets.toml.template" ".streamlit\secrets.toml"
            echo ✅ 配置文件模板已创建，请编辑 .streamlit\secrets.toml 文件
        ) else (
            echo ❌ 配置文件模板不存在
        )
    )
    pause
    exit /b 1
)

REM 运行测试
echo 🧪 运行系统测试...
python test_system.py
if %errorlevel% neq 0 (
    echo ❌ 系统测试失败，请检查配置
    pause
    exit /b 1
)

REM 启动应用
echo 🌟 启动批次报表生成器...
echo ----------------------------------------
echo 📝 提示：
echo    - 应用将在浏览器中自动打开
echo    - 默认地址: http://localhost:8501
echo    - 按 Ctrl+C 停止应用
echo ----------------------------------------

REM 启动 Streamlit 应用
streamlit run main.py --server.headless false --server.enableCORS false --server.enableXsrfProtection false

echo 👋 批次报表生成器已关闭
pause
