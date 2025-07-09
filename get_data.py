from database import Database_Config
from models import T_Device_Type, T_Device_Info, T_Batch, T_Device_Batch, T_TQ_Batch_Realtime, T_TQ_Batch_Archive
import pandas as pd
from sqlmodel import select, text
from typing import Optional, Any, cast


def get_device_info(database_config: Database_Config):
    with database_config.get_session() as session:
        query = text(f"select \
                     T_Device_Type.type_name as type_name,\
                     device_name, device_id, product_name, batch_number, device_state\
                     from T_Device_Info\
                     join T_Device_Type on T_Device_Info.device_type_id = T_Device_Type.device_type_id\
                     order by T_Device_Info.device_type_id, T_Device_Info.device_id")
        # device_info = (
        #     select(T_Device_Info.device_id,
        #            T_Device_Type.type_name,
        #            T_Device_Info.device_name,
        #            T_Device_Info.product_name,
        #            T_Device_Info.batch_number,
        #            T_Device_Info.device_state)
        #     .join(T_Device_Type, T_Device_Info.device_type_id == T_Device_Type.device_type_id)
        # )
        return pd.read_sql(query, session.connection())