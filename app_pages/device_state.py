import streamlit as st
from database_config import get_database_config
from get_data import get_device_info_df
from st_aggrid import AgGrid, GridOptionsBuilder, StAggridTheme, JsCode


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
                    {'field': 'device_state', 'headerName': '设备状态'}
                ],
                'autoSizeStrategy': {
                    'type': 'fitGridWidth',
                    'defaultMinWidth': 100
                },
                'defaultColDef': {
                    'sortable': False,
                    'filter': True,
                    'resizable': False,
                },
                # 自适应页宽
                "onGridReady": JS_ON_GRID_READY,
                "onFirstDataRendered": JS_ON_FIRST_DATA,
                "onGridSizeChanged": JS_ON_GRID_SIZE_CHANGED
                # 'autoSizeColumns': True
            }
            params = {
                "fontSize": 14,
                "rowBorder": True,
                'columnBorder': True,
                "backgroundColor": '#FFFFFF',
                'spacing': 4,
                'headerFontWeight': 'bold',
                'headerBackgroundColor': '#E6E6E6'
            }
            custom_theme = StAggridTheme(base='quartz').withParams(**params)

            # column_config = {
            #     "device_id": "设备编号",
            #     "type_name": "设备类型",
            #     "device_name": "设备名称",
            #     "product_name": "产品名称",
            #     "batch_number": "批次编号",
            #     "device_state": "设备状态"
            # }
            st.success("设备状态数据加载成功")
            # st.dataframe(results,
            #             use_container_width=True,
            #             hide_index=True,
            #             column_config=column_config)
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