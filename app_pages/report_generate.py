import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, StAggridTheme
from database_config import get_database_config
from get_data import get_device_type_tuple, get_device_tuple, get_report_data_df
from clean_data import get_report_template_dataframe
from report import get_report


# def render_report_sections(report_data):
#     for section in report_data['sections']:
#         # 标题
#         st.markdown(f"""
#         <div style="background-color: #f0f2f6; padding: 10px; 
#                     text-align: center; font-weight: bold; 
#                     border: 1px solid #ddd; margin: 10px 0;">
#             {section['title']}
#         </div>
#         """, unsafe_allow_html=True)
#         # 数据表格
#         st.dataframe(section['data'], use_container_width=True, hide_index=True)

def render_report_sections_to_aggrid(report_data):
    GRID_CSS = {
    ".ag-header": {"display": "none"},
    ".ag-center-cols-viewport": {
        "min-height": "unset !important"
    }
    }
    COMMON_COL_DEF = dict(
        editable=False,
        filter=False,
        sortable=False,
        resizable=True,
        wrapText=True,
        cellStyle={'textAlign': 'center'},
        # autoHeight=True
    )
    PARAMS = {
        "fontSize": 14,
        "rowBorder": True,
        'columnBorder': True,
        'wrapperBorder': True,
        'borderColor': "#666666",
        "backgroundColor": '#FFFFFF',
        'spacing': 4,
    }
    custom_theme = StAggridTheme(base='quartz').withParams(**PARAMS)
    for idx, sec in enumerate(report_data['sections']):
        # 段标题
        st.markdown(
            f"""
            <div style="
                background-color:#E6E6E6;padding:4px;
                text-align:center;font-weight:bold;
                border:1px solid #ddd;margin:10px 0;
                border-radius: 8px;
            ">
                {sec['title']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 表格
        gb = GridOptionsBuilder.from_dataframe(sec["data"])
        gb.configure_default_column(**COMMON_COL_DEF)
        # 行高比 DataFrame 略小一点，让外观更紧凑
        gb.configure_grid_options(
            # headerHeight=0,
            # rowHeight=28,
            pagination=False,
            suppressHorizontalScroll=True,
            domLayout="autoHeight",
            detailRowAutoHeight=True,
            autoSizeStrategy={
                'type': 'fitGridWidth',
            }
        )
        grid_opt = gb.build()

        AgGrid(
            sec["data"],
            gridOptions=grid_opt,
            custom_css=GRID_CSS,
            allow_unsafe_jscode=False,
            enable_enterprise_modules=False,
            theme=custom_theme,
            key=f"sec_{idx}"
        )


@st.fragment
def st_generate_report(report_template_df: dict, batch_number, device_name) -> None:
    generate_report_button = st.button('生成报表', icon=':material/table_convert:')
    if generate_report_button:
        # 转换新格式为旧格式以兼容报表生成器
        legacy_format = {
            'header': [report_template_df['sections'][0]['data']],  # 报表基本信息
            'main': [
                report_template_df['sections'][1]['data'],  # 一次参数设置
                report_template_df['sections'][2]['data']   # 一次煎煮记录
            ],
            'footer': [report_template_df['sections'][3]['data']]   # 汇总信息
        }
        
        batch_report = get_report(legacy_format, 'T_TQ_Batch_Archive', device_name)
        st.success("报表生成成功！")
        st.download_button(
            label='下载报表',
            data=batch_report,
            file_name=f'batch_report_{batch_number}.xlsx',
            on_click='ignore',
            icon=':material/download:',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


def page():
    database = get_database_config()
    report_template_df = None

    # st.title("报表生成")
    # st.markdown("---")
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4, vertical_alignment='bottom')
        with col1:
            # 选择设备类型
            device_type_tuples = get_device_type_tuple(database)
            device_type = st.selectbox(
                "**设备类型**",
                options=device_type_tuples,
                format_func=lambda x: x[1],
                index=None,
                accept_new_options=False
            )
            device_type_id = device_type[0] if device_type else 0
        with col2:
            # 选择设备
            device_tuples = get_device_tuple(database, device_type_id)
            device_id_select = st.selectbox(
                '**选择设备**',
                options=device_tuples if device_tuples else [],
                format_func=lambda x: x[1],
                index=None,
                accept_new_options=False
            )
            device_id = device_id_select[0] if device_id_select else 0
            device_name = device_id_select[1] if device_id_select else ""
        with col3:
            # 手动输入批次号
            batch_number = st.text_input("**批次号**", placeholder="请输入目标批次号")
        with col4:
            get_report_button = st.button("查询报表", icon=':material/search_insights:')

    if get_report_button:
        with st.container(border=True):
            if not device_type:
                st.warning("未选择设备类型")
            elif not device_id:
                st.warning("未选择设备")
            elif not batch_number:
                st.warning("未输入批次号")
            else:
                report_table_name, report_data_df = get_report_data_df(database, batch_number, device_id)
                if report_data_df is None or report_data_df.empty:
                    st.info("未找到相关报表数据")
                    return
                report_template_df = get_report_template_dataframe(report_table_name, report_data_df)
                if report_template_df is None or not report_template_df:
                    st.info("报表数据为空")
                    return
                # 使用通用渲染函数显示报表
                # render_report_sections(report_template_df)
                render_report_sections_to_aggrid(report_template_df)
    
    if report_template_df:
        with st.container(border=True):
            st_generate_report(report_template_df, batch_number, device_name)

    # 页脚
    st.markdown("---")
    st.markdown("© 2025 UWNTEK工程中心")