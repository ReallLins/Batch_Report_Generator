from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, NVARCHAR, DateTime, DECIMAL, ForeignKey
from typing import Optional

Base = declarative_base()

# 归档表基类
class TArchiveBase(Base):
    __abstract__ = True

    device_batch_id = Column(Integer, ForeignKey("T_Device_Batch.device_batch_id"), primary_key=True)
    device_id = Column(Integer, ForeignKey("T_Device_Info.device_id"), nullable = False)

class TDeviceType(Base):
    __tablename__ = "T_Device_Type"

    device_type_id = Column(Integer, primary_key=True, nullable=False)
    type_code = Column(NVARCHAR, nullable=False)
    type_name = Column(NVARCHAR, nullable=False)
    realtime_table_name = Column(NVARCHAR, nullable=False)
    archive_table_name = Column(NVARCHAR, nullable=False)

class TDeviceInfo(Base):
    __tablename__ = "T_Device_Info"

    device_id = Column(Integer, primary_key=True)
    device_type_id = Column(Integer, ForeignKey("T_Device_Type.device_type_id"), nullable=False)
    device_name = Column(NVARCHAR, nullable=False)
    product_name = Column(NVARCHAR, nullable=True)
    batch_number = Column(NVARCHAR, ForeignKey("T_Batch.batch_number"), nullable=True)
    device_state = Column(NVARCHAR, nullable=True)

class TBatch(Base):
    __tablename__ = "T_Batch"

    batch_number = Column(NVARCHAR, primary_key=True)
    product_name = Column(NVARCHAR, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    batch_state = Column(NVARCHAR, nullable=True)
    batch_quantity = Column(DECIMAL(10, 2), nullable=True)

class TDeviceBatch(Base):
    __tablename__ = "T_Device_Batch"

    device_batch_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("T_Device_Info.device_id"), unique=True)
    batch_number = Column(NVARCHAR, ForeignKey("T_Batch.batch_number"), unique=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    device_batch_state = Column(NVARCHAR, nullable=True)

class TTQBatchRealtime(Base):
    __tablename__ = "T_TQ_Batch_Realtime"

    device_batch_id = Column(Integer, ForeignKey("T_Device_Batch.device_batch_id"), nullable = False)
    device_id = Column(Integer, ForeignKey("T_Device_Info.device_id"), primary_key=True)
    # 一次煎煮设定参数
    p1_up_temp_set = Column(DECIMAL, nullable=True)
    p1_up_temp_press_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_press_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_time_set = Column(DECIMAL, nullable=True)
    p1_solvent_num_set = Column(DECIMAL, nullable=True)
    # 一次煎煮升温
    p1_up_temp_start_time = Column(DateTime, nullable=True)
    p1_up_temp_end_time = Column(DateTime, nullable=True)
    p1_up_temp_min_press = Column(DECIMAL, nullable=True)
    p1_up_temp_max_press = Column(DECIMAL, nullable=True)
    # 一次煎煮保温
    p1_hold_temp_start_time = Column(DateTime, nullable=True)
    p1_hold_temp_end_time = Column(DateTime, nullable=True)
    p1_hold_temp_min_press = Column(DECIMAL, nullable=True)
    p1_hold_temp_max_press = Column(DECIMAL, nullable=True)
    p1_hold_temp_time = Column(DECIMAL, nullable=True)
    p1_hold_temp_min_temp = Column(DECIMAL, nullable=True)
    p1_hold_temp_max_temp = Column(DECIMAL, nullable=True)
    # 一次煎煮溶媒和出液
    p1_solvent_num = Column(DECIMAL, nullable=True)
    p1_out_num = Column(DECIMAL, nullable=True)
    # 一次煎煮整体时间
    p1_start_time = Column(DateTime, nullable=True)
    p1_end_time = Column(DateTime, nullable=True)

class TTQBatchArchive(TArchiveBase):
    __tablename__ = "T_TQ_Batch_Archive"

    # 设备批次时间
    device_batch_start_time = Column(DateTime, nullable=True)
    device_batch_end_time = Column(DateTime, nullable=True)
    # 一次煎煮设定参数
    p1_up_temp_set = Column(DECIMAL, nullable=True)
    p1_up_temp_press_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_press_set = Column(DECIMAL, nullable=True)
    p1_hold_temp_time_set = Column(DECIMAL, nullable=True)
    p1_solvent_num_set = Column(DECIMAL, nullable=True)
    # 一次煎煮升温
    p1_up_temp_start_time = Column(DateTime, nullable=True)
    p1_up_temp_end_time = Column(DateTime, nullable=True)
    p1_up_temp_min_press = Column(DECIMAL, nullable=True)
    p1_up_temp_max_press = Column(DECIMAL, nullable=True)
    # 一次煎煮保温
    p1_hold_temp_start_time = Column(DateTime, nullable=True)
    p1_hold_temp_end_time = Column(DateTime, nullable=True)
    p1_hold_temp_min_press = Column(DECIMAL, nullable=True)
    p1_hold_temp_max_press = Column(DECIMAL, nullable=True)
    p1_hold_temp_time = Column(DECIMAL, nullable=True)
    p1_hold_temp_min_temp = Column(DECIMAL, nullable=True)
    p1_hold_temp_max_temp = Column(DECIMAL, nullable=True)
    # 一次煎煮溶媒和出液
    p1_solvent_num = Column(DECIMAL, nullable=True)
    p1_out_num = Column(DECIMAL, nullable=True)
    # 一次煎煮整体时间，可能用来获取历史序列值
    p1_start_time = Column(DateTime, nullable=True)
    p1_end_time = Column(DateTime, nullable=True)

class TSXBatchRealtime(Base):
    __tablename__ = "T_SX_Batch_Realtime"

    device_batch_id = Column(Integer, ForeignKey("T_Device_Batch.device_batch_id"), nullable = False)
    device_id = Column(Integer, ForeignKey("T_Device_Info.device_id"), primary_key=True)

class TSXBatchArchive(TArchiveBase):
    __tablename__ = "T_SX_Batch_Archive"



ARCHIVE_TABLE_MAPPING: dict[str, type[TArchiveBase]] = {
    'T_TQ_Batch_Archive': TTQBatchArchive,
    'T_SX_Batch_Archive': TSXBatchArchive
}

def get_archive_table_class(table_name: str) -> type[TArchiveBase]:
    table_class = ARCHIVE_TABLE_MAPPING.get(table_name)
    if not table_class:
        raise ValueError(f"不支持的归档表: {table_name}")
    return table_class

def get_supported_archive_classes() -> list[type[TArchiveBase]]:
    return list(ARCHIVE_TABLE_MAPPING.values())