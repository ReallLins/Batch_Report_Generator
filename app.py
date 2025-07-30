import streamlit as st
from streamlit_option_menu import option_menu
from app_pages import device_state, batch_query, report_generate


# device_state_page = st.Page('pages/device_state.py', title='设备状态', icon=':material/tv_options_input_settings:')
# batch_query_page = st.Page('pages/batch_query.py', title='批次查询', icon=':material/manage_search:')
# report_generate_page = st.Page('pages/report_generate.py', title='报表生成', icon=':material/table_convert:')
# pg = st.navigation([device_state_page, batch_query_page, report_generate_page])
st.set_page_config(page_title='批次报表工具', page_icon='icons/main_icon.png')
# pg.run()

# with st.sidebar:
#     col1, col2 = st.columns([1.2, 3])
#     with col1:
#         st.image('icons/main_icon.png', width=80, use_container_width=True)
#     with col2:
#         st.title('批次报表工具')

pages = [
    {'page': device_state.page, 'title': '设备状态', 'icon': 'gear'},
    {'page': batch_query.page, 'title': '批次查询', 'icon': 'card-list'},
    {'page': report_generate.page, 'title': '报表生成', 'icon': 'file-earmark-spreadsheet'}
]
titles = [p['title'] for p in pages]
icons = [p['icon'] for p in pages]


with st.sidebar:
    selected = option_menu(menu_title='批次报表工具',
                            menu_icon='house',
                            options=titles,
                            icons=icons,
                            default_index=0
                            )

for page in pages:
    if page['title'] == selected:
        page['page']()
        break
