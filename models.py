from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class T_Device_Type(SQLModel, table=True):
    device_type_id: int = Field(primary_key=True, nullable=False)
    type_code: str
    type_name: str
    realtime_table_name: str
    archive_table_name: str

class T_Device_Info(SQLModel, table=True):
    device_id: int = Field(primary_key=True)
    device_type_id: int = Field(nullable=False, foreign_key="T_Device_Type.device_type_id")
    device_name: str
    product_name: Optional[str] = None
    batch_number: Optional[str] = Field(foreign_key="T_Batch.batch_number")
    device_state: Optional[str] = None

class T_Batch(SQLModel, table=True):
    batch_number: str = Field(primary_key=True)
    product_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    batch_state: Optional[str] = None

class T_Device_Batch(SQLModel, table=True):
    device_batch_id: int = Field(primary_key=True)
    device_id: int = Field(unique=True, foreign_key="T_Device_Info.device_id")
    batch_number: str = Field(unique=True, foreign_key="T_Batch.batch_number")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    device_batch_state: Optional[str] = None

class T_TQ_Batch_Realtime(SQLModel, table=True):
    device_batch_id: int = Field(primary_key=True, foreign_key="T_Device_Batch.device_batch_id")
    device_id: int = Field(primary_key=True, foreign_key="T_Device_Info.device_id")
    # 一次煎煮设定参数
    p1_up_temp_set: Optional[Decimal] = None
    p1_up_temp_press_set: Optional[Decimal] = None
    p1_hold_temp_set: Optional[Decimal] = None
    p1_hold_temp_press_set: Optional[Decimal] = None
    p1_hold_temp_time_set: Optional[Decimal] = None
    p1_solvent_num_set: Optional[Decimal] = None
    # 升温过程
    p1_up_temp_start_time: Optional[datetime] = None
    p1_up_temp_end_time: Optional[datetime] = None
    p1_up_temp_min_press: Optional[Decimal] = None
    p1_up_temp_max_press: Optional[Decimal] = None
    # 保温过程
    p1_hold_temp_start_time: Optional[datetime] = None
    p1_hold_time_end_tme: Optional[datetime] = None
    p1_hold_temp_min_press: Optional[Decimal] = None
    p1_hold_temp_max_press: Optional[Decimal] = None
    p1_hold_temp_time: Optional[Decimal] = None
    p1_hold_temp_min_temp: Optional[Decimal] = None
    p1_hold_temp_max_temp: Optional[Decimal] = None
    # 溶媒和出液
    p1_solvent_num: Optional[Decimal] = None
    p1_out_num: Optional[Decimal] = None
    # 整体时间
    p1_start_time: Optional[datetime] = None
    p1_end_time: Optional[datetime] = None

class T_TQ_Batch_Archive(SQLModel, table=True):
    device_batch_id: int = Field(primary_key=True, foreign_key="T_Device_Batch.device_batch_id")
    device_id: int = Field(foreign_key="T_Device_Batch.device_id")
    # 设备批次时间
    device_batch_start_time: Optional[datetime] = None
    device_batch_end_time: Optional[datetime] = None
    # 一次煎煮设定参数
    p1_up_temp_set: Optional[Decimal] = None
    p1_up_temp_press_set: Optional[Decimal] = None
    p1_hold_temp_set: Optional[Decimal] = None
    p1_hold_temp_press_set: Optional[Decimal] = None
    p1_hold_temp_time_set: Optional[Decimal] = None
    p1_solvent_num_set: Optional[Decimal] = None
    # 升温过程
    p1_up_temp_start_time: Optional[datetime] = None
    p1_up_temp_end_time: Optional[datetime] = None
    p1_up_temp_min_press: Optional[Decimal] = None
    p1_up_temp_max_press: Optional[Decimal] = None
    # 保温过程
    p1_hold_temp_start_time: Optional[datetime] = None
    p1_hold_time_end_tme: Optional[datetime] = None
    p1_hold_temp_min_press: Optional[Decimal] = None
    p1_hold_temp_max_press: Optional[Decimal] = None
    p1_hold_temp_time: Optional[Decimal] = None
    p1_hold_temp_min_temp: Optional[Decimal] = None
    p1_hold_temp_max_temp: Optional[Decimal] = None
    # 溶媒和出液
    p1_solvent_num: Optional[Decimal] = None
    p1_out_num: Optional[Decimal] = None
    # 整体时间
    p1_start_time: Optional[datetime] = None
    p1_end_time: Optional[datetime] = None

