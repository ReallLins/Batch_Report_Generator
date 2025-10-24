from postgre_config import DatabaseConfig, get_database_config, get_engine

from models import TDeviceType, TDeviceInfo, TBatch, TDeviceBatch, TTQBatchRealtime, TTQBatchArchive, TSXBatchArchive
import pandas as pd
from sqlalchemy import select, text, Engine


# 基础方法
#获取设备类型
def get_device_type_df(database_config: DatabaseConfig, database_engine: Engine) -> pd.DataFrame:
    with database_config.get_session(database_engine) as session:
        device_type_query = (
            select(TDeviceType.device_type_id,
                   TDeviceType.type_name)
            .order_by(TDeviceType.device_type_id)
        )
        return pd.read_sql(device_type_query, session.connection())

database_config = get_database_config()
database_engine = get_engine(database_config)

device_type_df = get_device_type_df(database_config, database_engine)
print(device_type_df)