import streamlit as st
import pandas as pd
from database_config import get_database_config
from get_data import get_search_batchs_data, get_device_type_tuple, get_device_tuple
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, StAggridTheme
import streamlit.components.v1 as components
import streamlit_antd_components as sac
import traceback


def render_batch_table(realtime: bool, database, theme: StAggridTheme):
    key_suffix = 'rt' if realtime else 'his'
    with st.container(border=True, key=f"search_container_{key_suffix}"):
        cols1 = st.columns(3, vertical_alignment='bottom')
        cols2 = st.columns(3, vertical_alignment='bottom')
        with cols1[0]:
            batch_number = st.text_input("**批次号**", placeholder="请输入目标批次号", key=f"batch_number_{key_suffix}")
        with cols1[1]:
            device_type_tuples = get_device_type_tuple(database)
            device_type = st.selectbox(
                "**设备类型**",
                options=device_type_tuples,
                format_func=lambda x: x[1],
                index=None,
                accept_new_options=False,
                key=f"device_type_{key_suffix}"
            )
            device_type_id = device_type[0] if device_type else 0
        with cols1[2]:
            device_tuples = get_device_tuple(database, device_type_id)
            device_id_select = st.selectbox(
                '**选择设备**',
                options=device_tuples if device_tuples else [],
                format_func=lambda x: x[1],
                index=None,
                accept_new_options=False,
                key=f"device_id_{key_suffix}"
            )
            device_id = device_id_select[0] if device_id_select else 0
        with cols2[0]:
            start_time = cols2[0].date_input("**开始日期**", value=None, key=f"start_time_{key_suffix}")
        with cols2[1]:
            end_time = cols2[1].date_input("**结束日期**", value=None, key=f"end_time_{key_suffix}")
        with cols2[2]:
            search_button = st.button("查询批次", icon=':material/search_insights:', key=f"search_button_{key_suffix}")
    with st.container(key=f"batch_container_{key_suffix}"):
        if search_button:
            try:
                batch_df, device_df = get_search_batchs_data(
                    database,
                    batch_number,
                    device_id,
                    start_time.strftime('%Y-%m-%d') if start_time else None,
                    end_time.strftime('%Y-%m-%d') if end_time else None,
                    realtime=realtime
                )
                if batch_df.empty:
                    st.info("未查询到批次数据")
                    return
                # grid_options = GridOptionsBuilder.from_dataframe(batch_df)
                grid_options = {
                    "columnDefs": [
                        {"field": "batch_number", "headerName": "批次编号", "cellRenderer": "agGroupCellRenderer"},
                        {"field": "product_name", "headerName": "产品名称"},
                        {"field": "start_time", "headerName": "开始时间"},
                        {"field": "end_time", "headerName": "完成时间"},
                        {"field": "batch_state", "headerName": "批次状态"}
                    ],
                    "pagination": True,
                    "paginationPageSize": 20,
                    "cellSelection": True,
                    "defaultColDef": {
                        "sortable": False,
                        "filter": True,
                        "resizable": True,
                    },
                    "masterDetail": True,
                    # "isExternalFilterPresent": False,
                    # "doesExternalFilterPass": lambda node: True,
                    "detailRowHeight": 200,
                    "autoSizeStrategy": {
                        'type': 'fitGridWidth',
                        'defaultMinWidth': 20
                    },
                    "detailCellRendererParams": {
                        "detailGridOptions": {
                            "columnDefs": [
                                {"field": "device_id", "headerName": "设备ID"},
                                {"field": "device_name", "headerName": "设备名称"},
                                {"field": "device_state", "headerName": "设备状态"},
                            ],
                            "pagination": True,
                            "paginationPageSize": 20,
                            "defaultColDef": {
                                "sortable": False,
                                "filter": True,
                                "resizable": True,
                                "selectionMode": "single"
                            },
                            "autoSizeStrategy": {
                                'type': 'fitGridWidth',
                                'defaultMinWidth': 20
                            }
                        },
                        # JS 片段告诉 AG-Grid 如何把子表数据喂进去
                        "getDetailRowData": JsCode(
                            f"""
                            function(params) {{
                                // 通过 batch_number 过滤 device_df
                                const deviceData = {device_df.to_json(orient='records')};
                                const key = params.data.batch_number;
                                const devices = deviceData.filter(d => d.batch_number === key);
                                params.successCallback(devices);
                            }}
                            """
                        ),
                    }
                }
                # 把设备层数据从 pandas 转成 dict，给到 JS 全局
                # device_js = JsCode(f"window.deviceData_{key_suffix} = {device_df.to_json(orient='records')};")
                # device_js = device_df.to_json(orient='records')

                # 注入 device_df 到前端 JS 作用域
                # components.html(f"<script>{device_js}</script>", height=0)
                # components.html(f"<script>window.deviceData_{key_suffix} = {device_js};</script>", height=0)
                st.success("批次数据加载成功")
                AgGrid(
                    batch_df,
                    gridOptions=grid_options,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules=True,
                    theme=theme if theme else StAggridTheme(base='quartz'),
                    key=f"aggrid_{key_suffix}"
                )
                
                # st.dataframe(batch_df, use_container_width=True, hide_index=True)
                # st.dataframe(device_df, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"查询批次数据失败: {e}")
                st.error(f"{traceback.format_exc()}")
                return
def page():
    database = get_database_config()
    params = {
        "fontSize": 14,
        "rowBorder": True,
        'columnBorder': True,
        "backgroundColor": '#FFFFFF',
        'spacing': 4,
        'headerFontWeight': 'bold',
        # 'headerBackgroundColor': '#D4E3F6'
        'headerBackgroundColor': '#E6E6E6'
    }
    custom_theme = StAggridTheme(base='quartz').withParams(**params)

    # st.title("批次查询")
    # st.markdown("---")

    select = sac.tabs([sac.TabsItem(label='实时批次'),sac.TabsItem(label='历史批次')],
                      size='md', variant='outline',
                      align='start', color='#2E5FF3',
                      return_index=True
                    )

    if select == 0:
        # st.subheader("实时批次")
        render_batch_table(realtime=True, database=database, theme=custom_theme)

    if select == 1:
        # st.subheader("历史批次")
        render_batch_table(realtime=False, database=database, theme=custom_theme)

    # 页脚
    st.markdown("---")
    st.markdown("© 2025 UWNTEK工程中心")