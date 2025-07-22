import streamlit as st
from database_config import DatabaseConfig
from models import TBatch, TDeviceInfo, TDeviceType, TTQBatchArchive, TDeviceBatch
from sqlalchemy import select
import pandas as pd
import get_data
from clean_data import get_report_template_dataframe


db_host: str = st.secrets.db_conn.get('db_host')
db_port: str = st.secrets.db_conn.get('db_port')
db_name: str = st.secrets.db_conn.get('db_name')
db_username: str = st.secrets.db_conn.get('db_username')
db_password: str = st.secrets.db_conn.get('db_password')
database = DatabaseConfig(db_host, db_port, db_name, db_username, db_password)

# 配置页面
st.set_page_config(
    page_title="批次报表生成器",
    page_icon=".streamlit/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#     </style>
# """, unsafe_allow_html=True)

# 标题
st.title("📊 批次报表生成器")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("🔧 系统管理")
    st.markdown("---")
    st.header("📋 功能菜单")
    menu_option = st.selectbox(
        "选择功能",
        ["设备状态", "批次查询", "报表生成"]
    )

# 主内容区域
if menu_option == "批次查询":
    st.header("🔍 批次查询")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("查询条件")
        batch_number = st.text_input("批次号", placeholder="输入批次号进行查询")
        
        if st.button("查询批次"):
            if batch_number:
                try:
                    with database.get_session() as session:
                        # 查询批次信息
                        batch = session.get(TBatch, batch_number)
                        if batch:
                            st.success(f"找到批次: {batch_number}")
                            
                            # 显示批次详情
                            batch_data = {
                                "批次号": batch.batch_number,
                                "产品名称": batch.product_name,
                                "开始时间": batch.start_time,
                                "结束时间": batch.end_time,
                                "批次状态": batch.batch_state
                            }
                            
                            df = pd.DataFrame([batch_data]).T
                            df.columns = ["值"]
                            st.dataframe(df, use_container_width=True)
                            
                        else:
                            st.warning("未找到该批次号的记录")
                            
                except Exception as e:
                    st.error(f"查询失败: {e}")
            else:
                st.warning("请输入批次号")
    
    with col2:
        st.subheader("批次列表")
        try:
            with database.get_session() as session:
                # 获取最近的批次
                statement = select(TBatch).limit(10)
                batches = session.execute(statement).all()

                if batches:
                    batch_list = []
                    for batch in batches:
                        batch_list.append({
                            "批次号": batch.batch_number,
                            "产品名称": batch.product_name,
                            "状态": batch.batch_state or "未知",
                            "开始时间": batch.start_time
                        })
                    
                    df = pd.DataFrame(batch_list)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("暂无批次数据")
                    
        except Exception as e:
            st.error(f"获取批次列表失败: {e}")

elif menu_option == "设备状态":
    st.header("🏭 设备状态")
    try:
        results = get_data.get_device_info(database)
        if results is not None and not results.empty:
            column_config = {
                "device_id": "设备编号",
                "type_name": "设备类型",
                "device_name": "设备名称",
                "product_name": "产品名称",
                "batch_number": "批次号",
                "device_state": "设备状态"
            }
            st.success("设备状态数据加载成功")
            st.dataframe(results,
                         use_container_width=True,
                         hide_index=True,
                         column_config=column_config)
        else:
            st.info("暂无设备数据")
    except Exception as e:
        st.error(f"获取设备状态失败: {e}")

elif menu_option == "报表生成":
    st.header("📈 报表生成")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("报表配置")
        
        # 选择设备
        device_id = st.number_input("设备编号", min_value=1, value=1)
        
        # 手动输入批次号
        batch_number = st.text_input("批次号", placeholder="请输入要查询的批次号")
        
        # 选择报表类型
        report_type = st.selectbox(
            "报表类型",
            ["提取罐报表", "浓缩罐报表", "其他报表"]
        )
        
        if st.button("生成报表"):
            if not device_id:
                st.warning("请输入设备编号")
            elif not batch_number:
                st.warning("请输入批次号")
            elif report_type == "提取罐报表":
                try:
                    with database.get_session() as session:
                        # 先查询设备批次ID
                        device_batch_statement = select(TDeviceBatch).where(
                            (TDeviceBatch.device_id == device_id) & 
                            (TDeviceBatch.batch_number == batch_number)
                        )
                        device_batch = session.execute(device_batch_statement).first()
                        
                        if not device_batch:
                            st.warning(f"未找到设备编号 {device_id} 和批次号 {batch_number} 的关联记录")
                        else:
                            # 查询归档数据
                            archive_statement = select(TTQBatchArchive).where(
                                TTQBatchArchive.device_batch_id == device_batch.device_batch_id
                            )
                            archive_data = session.execute(archive_statement).first()
                            
                            # 查询设备信息
                            device_info = session.get(TDeviceInfo, device_id)
                            
                            # 查询批次信息
                            batch_info = session.get(TBatch, batch_number)
                            
                            if archive_data and device_info and batch_info:
                                st.success("报表数据加载成功")
                                
                                # 在右侧显示报表
                                with col2:
                                    st.subheader("📊 报表内容")
                                    
                                    # 基本信息
                                    st.markdown("### 基本信息")
                                    info_cols = st.columns(2)
                                    with info_cols[0]:
                                        st.metric("产品名称", batch_info.product_name or "未知")
                                        st.metric("批次号", batch_number)
                                    with info_cols[1]:
                                        st.metric("设备名称", device_info.device_name or "未知")
                                        st.metric("设备ID", device_id)
                                    
                                    # 工艺参数
                                    st.markdown("### 工艺参数")
                                    param_cols = st.columns(2)
                                    with param_cols[0]:
                                        st.metric("升温设定温度", f"{archive_data.p1_up_temp_set or 0}°C")
                                        st.metric("保温设定温度", f"{archive_data.p1_hold_temp_set or 0}°C")
                                    with param_cols[1]:
                                        st.metric("升温设定压力", f"{archive_data.p1_up_temp_press_set or 0} Bar")
                                        st.metric("保温设定压力", f"{archive_data.p1_hold_temp_press_set or 0} Bar")
                                    
                                    # 生产结果
                                    st.markdown("### 生产结果")
                                    result_cols = st.columns(2)
                                    with result_cols[0]:
                                        st.metric("溶媒设定量", f"{archive_data.p1_solvent_num_set or 0} L")
                                    with result_cols[1]:
                                        st.metric("实际出液量", f"{archive_data.p1_out_num or 0} L")
                                    
                                    # 时间信息
                                    st.markdown("### 时间信息")
                                    time_cols = st.columns(2)
                                    with time_cols[0]:
                                        st.info(f"开始时间: {archive_data.p1_start_time or '未知'}")
                                    with time_cols[1]:
                                        st.info(f"结束时间: {archive_data.p1_end_time or '未知'}")
                                    
                                    # 导出按钮
                                    if st.button("📥 导出Excel"):
                                        try:
                                            # 创建一个包含所需数据的报表对象
                                            from dataclasses import dataclass
                                            from typing import Optional
                                            from datetime import datetime
                                            from decimal import Decimal
                                            
                                            @dataclass
                                            class TempReportData:
                                                device_id: int
                                                device_name: Optional[str]
                                                product_name: Optional[str]
                                                batch_number: str
                                                # 工艺参数
                                                p1_up_temp_set: Optional[float]
                                                p1_up_temp_press_set: Optional[float]
                                                p1_hold_temp_set: Optional[float]
                                                p1_hold_temp_press_set: Optional[float]
                                                p1_solvent_num_set: Optional[float]
                                                # 生产过程
                                                p1_up_temp_start_time: Optional[datetime]
                                                p1_up_temp_end_time: Optional[datetime]
                                                p1_up_temp_min_press: Optional[float]
                                                p1_up_temp_max_press: Optional[float]
                                                p1_hold_temp_start_time: Optional[datetime]
                                                p1_hold_time_end_tme: Optional[datetime]
                                                p1_hold_temp_min_press: Optional[float]
                                                p1_hold_temp_max_press: Optional[float]
                                                # 生产结果
                                                p1_solvent_num: Optional[float]
                                                p1_out_num: Optional[float]
                                                p1_hold_temp_min_temp: Optional[float]
                                                p1_hold_temp_max_temp: Optional[float]
                                            
                                            def convert_decimal(value):
                                                """转换 Decimal 到 float"""
                                                if isinstance(value, Decimal):
                                                    return float(value)
                                                return value
                                            
                                            temp_report_data = TempReportData(
                                                device_id=device_id,
                                                device_name=device_info.device_name,
                                                product_name=batch_info.product_name,
                                                batch_number=batch_number,
                                                p1_up_temp_set=convert_decimal(archive_data.p1_up_temp_set),
                                                p1_up_temp_press_set=convert_decimal(archive_data.p1_up_temp_press_set),
                                                p1_hold_temp_set=convert_decimal(archive_data.p1_hold_temp_set),
                                                p1_hold_temp_press_set=convert_decimal(archive_data.p1_hold_temp_press_set),
                                                p1_solvent_num_set=convert_decimal(archive_data.p1_solvent_num_set),
                                                p1_up_temp_start_time=archive_data.p1_up_temp_start_time,
                                                p1_up_temp_end_time=archive_data.p1_up_temp_end_time,
                                                p1_up_temp_min_press=convert_decimal(archive_data.p1_up_temp_min_press),
                                                p1_up_temp_max_press=convert_decimal(archive_data.p1_up_temp_max_press),
                                                p1_hold_temp_start_time=archive_data.p1_hold_temp_start_time,
                                                p1_hold_time_end_tme=archive_data.p1_hold_time_end_tme,
                                                p1_hold_temp_min_press=convert_decimal(archive_data.p1_hold_temp_min_press),
                                                p1_hold_temp_max_press=convert_decimal(archive_data.p1_hold_temp_max_press),
                                                p1_solvent_num=convert_decimal(archive_data.p1_solvent_num),
                                                p1_out_num=convert_decimal(archive_data.p1_out_num),
                                                p1_hold_temp_min_temp=convert_decimal(archive_data.p1_hold_temp_min_temp),
                                                p1_hold_temp_max_temp=convert_decimal(archive_data.p1_hold_temp_max_temp),
                                            )
                                            
                                            # 使用现有的报表生成函数
                                            from report import generate_tq_report
                                            excel_data = generate_tq_report(temp_report_data)
                                            
                                            st.download_button(
                                                label="下载Excel文件",
                                                data=excel_data,
                                                file_name=f"提取罐报表_{batch_number}_{device_id}.xlsx",
                                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                            )
                                        except Exception as e:
                                            st.error(f"Excel导出失败: {e}")
                            else:
                                if not archive_data:
                                    st.warning(f"未找到设备批次ID {device_batch.device_batch_id} 的归档数据")
                                elif not device_info:
                                    st.warning(f"未找到设备ID {device_id} 的设备信息")
                                elif not batch_info:
                                    st.warning(f"未找到批次号 {batch_number} 的批次信息")
                                    
                except Exception as e:
                    st.error(f"生成报表失败: {e}")

# 页脚
st.markdown("---")
st.markdown("© 2025 批次报表生成器")


