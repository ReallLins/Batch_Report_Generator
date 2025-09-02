from st_aggrid import JsCode
import json


# Ag-Grid license key
LICENSE_KEY = '[v3][RELEASE][0102]_NDg2Njc4MzY3MDgzNw==16d78ca762fb5d2ff740aed081e2af7b'
DTIME_FORMAT = JsCode(
        """
        function(params){
            if(!params.value || params.value === 'NaT') return '';
            const v = (params.value instanceof Date)
                        ? params.value.toISOString().substring(0,19).replace('T',' ')
                        : String(params.value).replace('T',' ');
            return v;
        }
        """
)
JS_ON_GRID_READY = JsCode("""
    function(params){
        const fit = () => { if (params.api) { params.api.sizeColumnsToFit(); } };
        // 初次
        setTimeout(fit, 60);
        // 浏览器窗口变化
        window.addEventListener('resize', () => setTimeout(fit, 60));
        // 容器宽度变化（如侧边栏折叠/展开）
        if (window.ResizeObserver) {
            const ro = new ResizeObserver(() => setTimeout(fit, 60));
            ro.observe(params.eGridDiv);          // 观察当前网格容器
            const parent = params.eGridDiv.parentElement;
            if (parent) ro.observe(parent);        // 以及其父容器（Streamlit列/容器）
        }
    }
""")
JS_ON_FIRST_DATA = JsCode("""
    function(params){
        setTimeout(function(){
            if (params.api) { params.api.sizeColumnsToFit(); }
        }, 0);
    }
""")
JS_ON_GRID_SIZE_CHANGED = JsCode("""
    function(params){
        setTimeout(function(){
            if (params.api) { params.api.sizeColumnsToFit(); }
        }, 0);
    }
""")
DEVICE_STATUS_CONFIG = {
    '运行中': {
        'backgroundColor': "#b5ffc1",
        'color': "#05A13E",
        'border': '1.5px solid rgba(70, 227, 114, 0.2)',
        'symbol': '●'
    },
    '未运行': {
        'backgroundColor': 'rgba(255, 0, 0, 0.05)',
        'color': "#CC4242",
        'border': '1.5px solid rgba(255, 0, 0, 0.3)',
        'symbol': '●'
    },
    '已完成': {
        'backgroundColor': "#DDDDDD",
        'color': "#656565",
        'border': '1.5px solid rgba(91, 91, 91, 0.1)',
        'symbol': '●'
    }
}
DEVICE_STATUS_CELL_STYLE = JsCode(f"""
    function(params) {{
        const value = params.value;
        const config = {json.dumps(DEVICE_STATUS_CONFIG, ensure_ascii=False)};
        
        if (value && config[value]) {{
            return {{
                "display": "flex",
                "justify-content": "flex-start",
                "align-items": "center",
            }};
        }}
        return {{}};
    }}
""")
DEVICE_STATUS_CELL_RENDERER = JsCode(f"""
    class StatusCellRenderer {{
        init(params) {{
            this.eGui = document.createElement('div');
            const value = params.value;
            const config = {json.dumps(DEVICE_STATUS_CONFIG, ensure_ascii=False)};

            if (value && config[value]) {{
                // 设置标签的样式
                this.eGui.style.backgroundColor = config[value].backgroundColor;
                this.eGui.style.color = config[value].color;
                this.eGui.style.border = config[value].border;
                
                // --- 在这里调整标签样式 ---
                this.eGui.style.borderRadius = '50px'; // 圆角
                this.eGui.style.padding = '1px 8px';  // 内边距 (上下 左右)
                this.eGui.style.display = 'inline-block'; // 设置为行内块元素以应用宽高
                this.eGui.style.fontWeight = 'middle';
                this.eGui.style.fontSize = '14px'; // 字体大小
                this.eGui.style.lineHeight = '20px'; // 行高
                // --------------------------

                this.eGui.innerHTML = config[value].symbol + ' ' + value;
            }} else {{
                this.eGui.innerHTML = value || '';
            }}
        }}

        getGui() {{
            return this.eGui;
        }}

        refresh(params) {{
            return false;
        }}
    }}
""")
DETAIL_DEVICE_STATUS_CELL_RENDERER = JsCode(f"""
    class StatusCellRenderer {{
        init(params) {{
            this.eGui = document.createElement('div');
            const value = params.value;
            const config = {json.dumps(DEVICE_STATUS_CONFIG, ensure_ascii=False)};

            if (value && config[value]) {{
                // 设置标签的样式
                this.eGui.style.backgroundColor = config[value].backgroundColor;
                this.eGui.style.color = config[value].color;
                this.eGui.style.border = config[value].border;
                
                // --- 在这里调整标签样式 ---
                this.eGui.style.borderRadius = '50px'; // 圆角
                this.eGui.style.padding = '1px 8px';  // 内边距 (上下 左右)
                this.eGui.style.display = 'inline-block'; // 设置为行内块元素以应用宽高
                this.eGui.style.fontWeight = 'middle';
                this.eGui.style.fontSize = '12px'; // 字体大小
                this.eGui.style.lineHeight = '14px'; // 行高
                // --------------------------

                this.eGui.innerHTML = config[value].symbol + ' ' + value;
            }} else {{
                this.eGui.innerHTML = value || '';
            }}
        }}

        getGui() {{
            return this.eGui;
        }}

        refresh(params) {{
            return false;
        }}
    }}
""")


