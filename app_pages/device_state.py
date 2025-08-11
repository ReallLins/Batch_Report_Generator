import streamlit as st
from database_config import get_database_config
from get_data import get_device_info_df
from st_aggrid import AgGrid, GridOptionsBuilder, StAggridTheme, JsCode
import json


def page():
    # with st.sidebar:
    #     col1, col2 = st.columns([1.2, 3])
    #     with col1:
    #         st.image('icons/main_icon.png', width=80, use_container_width=True)
    #     with col2:
    #         st.title('批次报表工具')
    database = get_database_config()
    LICENSE_KEY = '[v3][RELEASE][0102]_NDg2Njc4MzY3MDgzNw==16d78ca762fb5d2ff740aed081e2af7b'
    # 新增：统一的列宽自适应脚本（主表/子表复用）
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
                if (parent) ro.observe(parent);        // 以及其父容器(Streamlit列/容器)
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
    # cellStyle
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
    # 自定义
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

    # st.title("设备状态")
    # st.markdown("---")
    try:
        results = get_device_info_df(database)
        if results is not None and not results.empty:
            grid_options = {
                'columnDefs': [
                    {'field': 'type_name', 'headerName': '设备类型'},
                    {'field': 'device_name', 'headerName': '设备名称'},
                    {'field': 'device_id', 'headerName': '设备编号'},
                    {'field': 'product_name', 'headerName': '产品名称'},
                    {'field': 'batch_number', 'headerName': '批次编号'},
                    {'field': 'device_state', 'headerName': '设备状态',
                     'cellRenderer': DEVICE_STATUS_CELL_RENDERER,
                     'cellStyle': DEVICE_STATUS_CELL_STYLE
                     }
                ],
                'autoSizeStrategy': {
                    'type': 'fitGridWidth'
                },
                'defaultColDef': {
                    'sortable': False,
                    'filter': True,
                    'resizable': True,
                    'cellStyle': {'display': 'flex', 'alignItems': 'center'}
                },
                "rowHeight": 40,
                "cell-align-items": "center",
                # 自适应页宽
                "onGridReady": JS_ON_GRID_READY,
                "onFirstDataRendered": JS_ON_FIRST_DATA,
                "onGridSizeChanged": JS_ON_GRID_SIZE_CHANGED
                # 'autoSizeColumns': True
            }
            params = {
                "fontSize": 14,
                "rowBorder": True,
                'columnBorder': False,
                "backgroundColor": '#FFFFFF',
                'spacing': 4,
                'headerFontWeight': 'bold',
                'headerBackgroundColor': '#E6E6E6'
            }
            custom_theme = StAggridTheme(base='quartz').withParams(**params)

            st.success("设备状态数据加载成功")
            AgGrid(results, 
                   gridOptions=grid_options, 
                   allow_unsafe_jscode=True,
                   enable_enterprise_modules=True, 
                   license_key=LICENSE_KEY,
                   theme=custom_theme)
        else:
            st.info("暂无设备数据")
    except Exception as e:
        st.error(f"获取设备状态失败: {e}")

    # 页脚
    st.markdown("---")
    st.markdown("© 2025 UWNTEK工程中心")