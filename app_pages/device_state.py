import streamlit as st
from database_config import get_database_config
from get_data import get_device_info_df
from st_aggrid import AgGrid, GridOptionsBuilder, StAggridTheme


def page():
    # with st.sidebar:
    #     col1, col2 = st.columns([1.2, 3])
    #     with col1:
    #         st.image('icons/main_icon.png', width=80, use_container_width=True)
    #     with col2:
    #         st.title('批次报表工具')
    database = get_database_config()
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
            AgGrid(results, gridOptions=grid_options, enable_enterprise_modules=True, theme=custom_theme)
        else:
            st.info("暂无设备数据")
    except Exception as e:
        st.error(f"获取设备状态失败: {e}")

    # 页脚
    st.markdown("---")
    st.markdown("© 2025 UWNTEK工程中心")