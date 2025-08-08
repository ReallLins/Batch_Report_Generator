from database_config import DatabaseConfig
from models import TDeviceType, TDeviceInfo, TBatch, TDeviceBatch, TTQBatchRealtime, TTQBatchArchive, TSXBatchArchive
from models import get_archive_table_class
import pandas as pd
from sqlalchemy import select, text


# 基础方法
#获取设备类型
def get_device_type_df(database_config: DatabaseConfig) -> pd.DataFrame:
    with database_config.get_session() as session:
        device_type_query = (
            select(TDeviceType.device_type_id,
                   TDeviceType.type_name)
            .order_by(TDeviceType.device_type_id)
        )
        return pd.read_sql(device_type_query, session.connection())

# 获取指定设备类型的设备
def get_device_df(database_config: DatabaseConfig, device_type_id: int = 0) -> pd.DataFrame:
    with database_config.get_session() as session:
        device_list_query = (
            select(TDeviceInfo.device_id,
                TDeviceInfo.device_name)
            .where(TDeviceInfo.device_type_id == device_type_id)
            .order_by(TDeviceInfo.device_id)
        )
        return pd.read_sql(device_list_query, session.connection())

# 获取设备信息
def get_device_info_df(database_config: DatabaseConfig) -> pd.DataFrame:
    with database_config.get_session() as session:
        device_info_query = (
            select(TDeviceType.type_name,
                TDeviceInfo.device_id,
                TDeviceInfo.device_name,
                TDeviceInfo.product_name,
                TDeviceInfo.batch_number,
                TDeviceInfo.device_state)
            .join(TDeviceType, TDeviceInfo.device_type_id == TDeviceType.device_type_id)
            .order_by(TDeviceInfo.device_type_id, TDeviceInfo.device_id)
        )
        return pd.read_sql(device_info_query, session.connection())

# 获取批次信息
def get_batch_info_df(database_config: DatabaseConfig) -> pd.DataFrame:
    with database_config.get_session() as session:
        batch_info_query = (
            select(TBatch.batch_number,
                   TBatch.product_name,
                   TBatch.start_time,
                   TBatch.end_time,
                   TBatch.batch_state)
            .order_by(TBatch.start_time.desc())
        )
        return pd.read_sql(batch_info_query, session.connection())

# 工厂方法
# 获取报表数据
def get_report_data_df(database_config: DatabaseConfig, batch_number: str, device_id: int):
    with database_config.get_session() as session:
        report_table_name_query = (
            select(TDeviceType.archive_table_name)
            .join(TDeviceInfo, TDeviceInfo.device_type_id == TDeviceType.device_type_id)
            .where(TDeviceInfo.device_id == device_id)
        )
        report_table_name_str = session.execute(report_table_name_query).scalar_one_or_none()
        if not report_table_name_str:
            raise ValueError(f"未找到设备ID {device_id} 的报表表名")
        report_table_name = get_archive_table_class(report_table_name_str)

        device_batch_id_query = (
            select(TDeviceBatch.device_batch_id)
            .where(TDeviceBatch.device_id == device_id, TDeviceBatch.batch_number == batch_number)
        )
        device_batch_id = session.execute(device_batch_id_query).scalar_one_or_none()
        if not device_batch_id:
            raise ValueError(f"设备ID {device_id}  批次号 {batch_number}  设备批次不存在")

        batch_info_query = (
            select(TBatch.batch_number,
                   TBatch.product_name,
                   TBatch.batch_quantity,
                   TBatch.start_time,
                   TBatch.end_time)
            .where(TBatch.batch_number == batch_number)
        )

        device_info_query = (
            select(TDeviceInfo.device_id,
                   TDeviceInfo.device_name)
            .where(TDeviceInfo.device_id == device_id)
        )

        report_data_query = (
            select(report_table_name,
                   TDeviceInfo.device_id,
                   TDeviceInfo.device_name,
                   TBatch.batch_number,
                   TBatch.product_name,
                   TBatch.batch_quantity,
                   TBatch.start_time,
                   TBatch.end_time)
            .select_from(report_table_name)
            .join(TDeviceInfo, TDeviceInfo.device_id == device_id)
            .join(TBatch, TBatch.batch_number == batch_number)
            .where(report_table_name.device_batch_id == device_batch_id)
        )
        report_data_df = pd.read_sql(report_data_query, session.connection())
        if report_data_df.empty:
            raise ValueError(f"设备ID {device_id}  批次号 {batch_number}  报表数据不存在")
        
        return report_table_name_str, report_data_df

# 获取设备类型下拉框使用的(id, name)元组列表
def get_device_type_tuple(database_config: DatabaseConfig) -> list[tuple]:
    device_types_df = get_device_type_df(database_config)
    device_type_tuple = list(zip(device_types_df['device_type_id'], device_types_df['type_name']))
    return device_type_tuple

# 获取设备下拉框使用的(id, name)元组列表
def get_device_tuple(database_config: DatabaseConfig, device_type_id: int = 0) -> list[tuple]:
    device_df = get_device_df(database_config, device_type_id)
    device_tuple = list(zip(device_df['device_id'], device_df['device_name']))
    return device_tuple

# 条件联合查询批次
def get_search_batchs_data(
        database_config: DatabaseConfig,
        batch_number: str,
        device_id: int,
        start_time: str | None,
        end_time: str | None,
        realtime: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    batch_query = """
        SELECT  b.batch_number,
                b.product_name,
                b.start_time,
                b.end_time,
                b.batch_state,
                b.batch_quantity,
                di.device_id,
                di.device_name,
                di.device_state,
                db.start_time AS device_batch_start_time,
                db.end_time AS device_batch_end_time
        FROM    T_Batch b
        LEFT JOIN T_Device_Batch db ON b.batch_number = db.batch_number
        LEFT JOIN T_Device_Info di ON db.device_id = di.device_id
        WHERE 1=1
    """
    params = {}
    if batch_number:
        batch_query += " AND b.batch_number LIKE %(batch_number)s"
        params['batch_number'] = batch_number
    if device_id:
        batch_query += " AND di.device_id = %(device_id)s"
        params['device_id'] = device_id
    if start_time:
        batch_query += " AND b.start_time >= %(start_time)s"
        params['start_time'] = start_time
    if end_time:
        batch_query += " AND (b.end_time <= %(end_time)s OR b.end_time IS NULL)"
        params['end_time'] = end_time
    if realtime:
        batch_query += " AND b.end_time IS NULL"
    else:
        batch_query += " AND b.end_time IS NOT NULL"
    batch_query += " ORDER BY b.start_time DESC"
    with database_config.get_session() as session:
        result = pd.read_sql(batch_query, session.connection(), params=params)
        if result.empty:
            return pd.DataFrame(), pd.DataFrame()
        batch_cols = ["batch_number", "product_name", "batch_quantity", "start_time", "end_time", "batch_state"]
        batch_df = result[batch_cols].drop_duplicates().reset_index(drop=True)
        device_cols = ["product_name", "batch_quantity", "start_time", "end_time", "batch_state"]
        device_df = result.drop(columns=device_cols)
        return batch_df, device_df
