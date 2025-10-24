from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, NVARCHAR, DateTime, DECIMAL, ForeignKey
from typing import Optional

Base = declarative_base()

# 归档表基类
class TArchiveBase(Base):
    __abstract__ = True

    device_batch_id = Column(Integer, ForeignKey("t_device_batch.device_batch_id"), primary_key=True)
    device_id = Column(Integer, ForeignKey("t_device_info.device_id"), nullable = False)

class TDeviceType(Base):
    __tablename__ = "t_device_type"

    device_type_id = Column(Integer, primary_key=True, nullable=False)
    type_code = Column(NVARCHAR, nullable=False)
    type_name = Column(NVARCHAR, nullable=False)
    realtime_table_name = Column(NVARCHAR, nullable=False)
    archive_table_name = Column(NVARCHAR, nullable=False)

class TDeviceInfo(Base):
    __tablename__ = "t_device_info"

    device_id = Column(Integer, primary_key=True)
    device_type_id = Column(Integer, ForeignKey("t_device_type.device_type_id"), nullable=False)
    device_name = Column(NVARCHAR, nullable=False)
    product_name = Column(NVARCHAR, nullable=True)
    batch_number = Column(NVARCHAR, ForeignKey("t_batch.batch_number"), nullable=True)
    device_state = Column(NVARCHAR, nullable=True)

class TBatch(Base):
    __tablename__ = "t_batch"

    batch_number = Column(NVARCHAR, primary_key=True)
    product_name = Column(NVARCHAR, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    batch_state = Column(NVARCHAR, nullable=True)
    batch_quantity = Column(DECIMAL(10, 2), nullable=True)

class TDeviceBatch(Base):
    __tablename__ = "t_device_batch"

    device_batch_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("t_device_info.device_id"), unique=True)
    batch_number = Column(NVARCHAR, ForeignKey("t_batch.batch_number"), unique=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    device_batch_state = Column(NVARCHAR, nullable=True)

class TTQBatchRealtime(Base):
    __tablename__ = "t_tq_batch_realtime"

    device_batch_id = Column(Integer, ForeignKey("t_device_batch.device_batch_id"), nullable = False)
    device_id = Column(Integer, ForeignKey("t_device_info.device_id"), primary_key=True)
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
    __tablename__ = "t_tq_batch_archive"

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
    # 一次煎煮整体时间，可能用来获取时序数据
    p1_start_time = Column(DateTime, nullable=True)
    p1_end_time = Column(DateTime, nullable=True)

class TSXBatchRealtime(Base):
    __tablename__ = "t_sx_batch_realtime"

    device_batch_id = Column(Integer, ForeignKey("t_device_batch.device_batch_id"), nullable = False)
    device_id = Column(Integer, ForeignKey("t_device_info.device_id"), primary_key=True)

class TSXBatchArchive(TArchiveBase):
    __tablename__ = "t_sx_batch_archive"



ARCHIVE_TABLE_MAPPING: dict[str, type[TArchiveBase]] = {
    't_tq_batch_archive': TTQBatchArchive,
    't_sx_batch_archive': TSXBatchArchive
}

def get_archive_table_class(table_name: str) -> type[TArchiveBase]:
    table_class = ARCHIVE_TABLE_MAPPING.get(table_name)
    if not table_class:
        raise ValueError(f"不支持的归档表: {table_name}")
    return table_class

def get_supported_archive_classes() -> list[type[TArchiveBase]]:
    return list(ARCHIVE_TABLE_MAPPING.values())