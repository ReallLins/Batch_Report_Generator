import streamlit as st
from database_config import get_database_config
from get_data import get_search_batchs_data, get_device_type_tuple, get_device_tuple
from clean_data import get_formatted_datetime_df
from st_aggrid import AgGrid, JsCode, StAggridTheme
import streamlit_antd_components as sac
import traceback
import json


def render_batch_table(realtime: bool, database, theme: StAggridTheme):
    key_suffix = 'rt' if realtime else 'his'
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
        if realtime:
            end_time = None
            with cols2[0]:
                start_time = st.date_input("**开始日期**", value=None, key=f"start_time_{key_suffix}")
            with cols2[1]:
                search_button = st.button("查询批次", icon=':material/search_insights:', key=f"search_button_{key_suffix}")
        else:
            with cols2[0]:
                start_time = st.date_input("**开始日期**", value=None, key=f"start_time_{key_suffix}")
            with cols2[1]:
                end_time = st.date_input("**结束日期**", value=None, key=f"end_time_{key_suffix}")
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
                # AG-Grid无法处理时间格式中的NaT，所以提前清洗为None
                batch_df = get_formatted_datetime_df(batch_df)
                device_df = get_formatted_datetime_df(device_df)
                device_df_json = device_df.to_json(orient='records', date_format='iso', date_unit='s')
                device_df_js = json.dumps(json.loads(device_df_json), ensure_ascii=False)
                grid_options = {
                    "columnDefs": [
                        {"field": "batch_number", "headerName": "批次编号", "cellRenderer": "agGroupCellRenderer"},
                        {"field": "product_name", "headerName": "产品名称"},
                        {"field": "batch_quantity", "headerName": "计划产量"},
                        {"field": "start_time", "headerName": "开始时间",
                         "type": ["dateColumnFilter", "customDateTimeFormat"],
                         "custom_format_string": "yyyy-MM-dd HH:mm:ss"},
                        {"field": "end_time", "headerName": "完成时间",
                         "type": ["dateColumnFilter", "customDateTimeFormat"],
                         "custom_format_string": "yyyy-MM-dd HH:mm:ss"},
                        {"field": "batch_state", "headerName": "批次状态"}
                    ],
                    "pagination": True,
                    "paginationPageSize": 20,
                    "cellSelection": True,
                    "defaultColDef": {
                        "sortable": False,
                        "filter": True,
                        "resizable": True
                    },
                    "masterDetail": True,
                    # "isExternalFilterPresent": False,
                    # "doesExternalFilterPass": lambda node: True,
                    "detailRowHeight": 200,
                    "autoSizeStrategy": {
                        'type': 'fitGridWidth',
                        'defaultMinWidth': 20
                    },
                    # 新增：主表的自适应钩子（不使用 domLayout:autoHeight）
                    "onGridReady": JS_ON_GRID_READY,
                    "onFirstDataRendered": JS_ON_FIRST_DATA,
                    "onGridSizeChanged": JS_ON_GRID_SIZE_CHANGED,
                    "detailCellRendererParams": {
                        "detailGridOptions": {
                            "columnDefs": [
                                {"field": "device_id", "headerName": "设备ID"},
                                {"field": "device_name", "headerName": "设备名称"},
                                {"field": "device_state", "headerName": "设备状态"},
                                {"field": "device_batch_start_time", "headerName": "开始时间",
                                 "valueFormatter": DTIME_FORMAT},
                                {"field": "device_batch_end_time", "headerName": "完成时间",
                                 "valueFormatter": DTIME_FORMAT}
                            ],
                            "pagination": True,
                            "paginationPageSize": 20,
                            "defaultColDef": {
                                "sortable": False,
                                "filter": False,
                                "resizable": True,
                                "selectionMode": "single"
                            },
                            "autoSizeStrategy": {
                                'type': 'fitGridWidth',
                                'defaultMinWidth': 20
                            },
                            # 新增：子表也自适应
                            "onGridReady": JS_ON_GRID_READY,
                            "onFirstDataRendered": JS_ON_FIRST_DATA,
                            "onGridSizeChanged": JS_ON_GRID_SIZE_CHANGED
                        },
                        # JS片段告诉AG-Grid如何把子表数据喂进去
                        "getDetailRowData": JsCode(
                            f"""
                            function(params) {{
                                // 通过 batch_number 过滤 device_df
                                const deviceData = {device_df_js};
                                const key = params.data.batch_number;
                                const devices = deviceData.filter(d => d.batch_number === key);
                                params.successCallback(devices);
                            }}
                            """
                        )
                    }
                }
                st.success("批次数据加载成功")
                AgGrid(
                    batch_df,
                    gridOptions=grid_options,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules=True,
                    license_key=LICENSE_KEY,
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