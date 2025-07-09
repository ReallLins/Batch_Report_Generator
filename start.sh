#!/bin/bash

# 批次报表生成器启动脚本
# Batch Report Generator Startup Script

echo "🚀 批次报表生成器启动脚本"
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装Python3"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 检查依赖
echo "🔍 检查依赖..."
if ! python3 -c "import streamlit, sqlmodel, openpyxl, pandas" 2>/dev/null; then
    echo "⚠️  缺少依赖，正在安装..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 检查配置文件
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  数据库配置文件不存在"
    echo "请创建 .streamlit/secrets.toml 文件并配置数据库连接信息"
    echo "参考模板: .streamlit/secrets.toml.template"
    
    read -p "是否要创建配置文件模板？ (y/n): " create_config
    if [ "$create_config" = "y" ] || [ "$create_config" = "Y" ]; then
        mkdir -p .streamlit
        if [ -f ".streamlit/secrets.toml.template" ]; then
            cp .streamlit/secrets.toml.template .streamlit/secrets.toml
            echo "✅ 配置文件模板已创建，请编辑 .streamlit/secrets.toml 文件"
        else
            echo "❌ 配置文件模板不存在"
        fi
    fi
    exit 1
fi

# 运行测试
echo "🧪 运行系统测试..."
python3 test_system.py
if [ $? -ne 0 ]; then
    echo "❌ 系统测试失败，请检查配置"
    exit 1
fi

# 启动应用
echo "🌟 启动批次报表生成器..."
echo "----------------------------------------"
echo "📝 提示："
echo "   - 应用将在浏览器中自动打开"
echo "   - 默认地址: http://localhost:8501"
echo "   - 按 Ctrl+C 停止应用"
echo "----------------------------------------"

# 启动 Streamlit 应用
streamlit run main.py --server.headless false --server.enableCORS false --server.enableXsrfProtection false

echo "👋 批次报表生成器已关闭"
