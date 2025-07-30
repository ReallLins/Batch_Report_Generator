import streamlit as st
import pandas as pd
from sqlalchemy import select
from database_config import get_database_config
from models import TBatch
from get_data import get_batch_info_df


def page():
    database = get_database_config()

    # st.title("批次查询")
    # st.markdown("---")

    tab_realtime, tab_archive = st.tabs(['**实时批次**', '**历史批次**'])

    with tab_realtime:
        # st.subheader("实时批次")
        # 这里可以添加实时批次的查询逻辑
        pass

    with tab_archive:
        # st.subheader("历史批次")
        # 这里可以添加历史批次的查询逻辑
        pass

    # 页脚
    st.markdown("---")
    st.markdown("© 2025 UWNTEK工程中心")