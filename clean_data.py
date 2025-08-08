import pandas as pd
from dataclasses import dataclass
from typing import Optional, Dict, Any, Protocol, runtime_checkable
from datetime import datetime

@runtime_checkable
class BaseReportDataProtocol(Protocol):
    # 通用基本参数
    product_name: Optional[str]
    batch_quantity: Optional[float]
    batch_number: Optional[str]
    device_batch_id: Optional[int]
    device_name: Optional[str]
    device_id: Optional[int]
    device_batch_start_time: Optional[str]
    device_batch_end_time: Optional[str]

# 提取罐报表数据类型协议
@runtime_checkable
class TQReportDataProtocol(BaseReportDataProtocol, Protocol):
    # 一次煎煮设定参数
    p1_up_temp_set: Optional[float]
    p1_up_temp_press_set: Optional[float]
    p1_hold_temp_set: Optional[float]
    p1_hold_temp_press_set: Optional[float]
    p1_hold_temp_time_set: Optional[float]
    p1_solvent_num_set: Optional[float]
    # 一次煎煮升温
    p1_up_temp_start_time: Optional[str]
    p1_up_temp_end_time: Optional[str]
    p1_up_temp_min_press: Optional[float]
    p1_up_temp_max_press: Optional[float]
    # 一次煎煮保温
    p1_hold_temp_start_time: Optional[str]
    p1_hold_temp_end_time: Optional[str]
    p1_hold_temp_min_press: Optional[float]
    p1_hold_temp_max_press: Optional[float]
    p1_hold_temp_time: Optional[float]
    p1_hold_temp_min_temp: Optional[float]
    p1_hold_temp_max_temp: Optional[float]
    # 一次煎煮溶媒和出液
    p1_solvent_num: Optional[float]
    p1_out_num: Optional[float]
    # 一次煎煮整体时间
    p1_start_time: Optional[str]
    p1_end_time: Optional[str]

# 双效浓缩器报表数据类型协议
@runtime_checkable
class SXReportDataProtocol(BaseReportDataProtocol, Protocol):
    # 双效浓缩器特有参数可以在这里定义
    pass

@dataclass
class BaseReportData:
    product_name: Optional[str] = ''
    batch_quantity: Optional[float] = None
    batch_number: Optional[str] = ''
    device_batch_id: Optional[int] = None
    device_name: Optional[str] = ''
    device_id: Optional[int] = None
    device_batch_start_time: Optional[str] = None
    device_batch_end_time: Optional[str] = None

@dataclass
class TQReportData(BaseReportData, TQReportDataProtocol):
    # 一次煎煮设定参数
    p1_up_temp_set: Optional[float] = 0.0
    p1_up_temp_press_set: Optional[float] = 0.0
    p1_hold_temp_set: Optional[float] = 0.0
    p1_hold_temp_press_set: Optional[float] = 0.0
    p1_hold_temp_time_set: Optional[float] = 0.0
    p1_solvent_num_set: Optional[float] = 0.0
    # 一次煎煮升温
    p1_up_temp_start_time: Optional[str] = None
    p1_up_temp_end_time: Optional[str] = None
    p1_up_temp_min_press: Optional[float] = 0.0
    p1_up_temp_max_press: Optional[float] = 0.0
    # 一次煎煮保温
    p1_hold_temp_start_time: Optional[str] = None
    p1_hold_temp_end_time: Optional[str] = None
    p1_hold_temp_min_press: Optional[float] = 0.0
    p1_hold_temp_max_press: Optional[float] = 0.0
    p1_hold_temp_time: Optional[float] = 0.0
    p1_hold_temp_min_temp: Optional[float] = 0.0
    p1_hold_temp_max_temp: Optional[float] = 0.0
    # 一次煎煮溶媒和出液
    p1_solvent_num: Optional[float] = 0.0
    p1_out_num: Optional[float] = 0.0
    # 一次煎煮整体时间
    p1_start_time: Optional[str] = None
    p1_end_time: Optional[str] = None

@dataclass
class SXReportData(BaseReportData, SXReportDataProtocol):
    # 双效浓缩器特有参数可以在这里定义
    pass

# 基础数据清洗工具
class DataCleaner:
    _NULL_LITERALS = {"", "null", "none", "nan", "n/a"}

    # 公共判空
    @staticmethod
    def _is_null(v: Any) -> bool:
        return (
            v is None
            or pd.isna(v)
            or (isinstance(v, str) and v.strip().lower() in DataCleaner._NULL_LITERALS)
        )

    # 数值
    @staticmethod
    def clean_float_value(v: Any) -> Optional[float]:
        if DataCleaner._is_null(v):
            return None
        try:
            return float(str(v).replace(",", ""))
        except ValueError:
            return None

    @staticmethod
    def clean_int_value(v: Any) -> Optional[int]:
        # 整数
        f = DataCleaner.clean_float_value(v)
        if f is None:
            return None
        if f.is_integer():
            return int(f)
        # 非整数时返回 None，也可以改成 round(f)
        return None

    # 时间
    @staticmethod
    def clean_datetime_value(v: Any) -> Optional[str]:
        if DataCleaner._is_null(v):
            return None
        ts = pd.to_datetime(v, errors="coerce")
        if pd.isna(ts):
            return None
        return ts.strftime("%Y-%m-%d %H:%M:%S")

    # 字符串
    @staticmethod
    def clean_str_value(v: Any) -> Optional[str]:
        if DataCleaner._is_null(v):
            return None
        return str(v).strip()
    
    # DataFrame 中的时间列格式化
    @staticmethod
    def format_datetime_value(df: pd.DataFrame) -> pd.DataFrame:
        time_cols = df.select_dtypes(include="datetime64[ns]").columns
        df[time_cols] = (
            df[time_cols]
            .astype("object")          # → object
            .where(df[time_cols].notna(), None)
        )
        return df

# 提取罐数据清洗
class TQDataCleaner:
    @staticmethod
    def clean_dataframe(raw_df: pd.DataFrame) -> TQReportData:
        if raw_df.empty:
            raise ValueError('提取罐报表数据为空！')
        data_dict = raw_df.iloc[0].to_dict()
        return TQReportData(
            product_name = DataCleaner.clean_str_value(data_dict.get('product_name')),
            batch_quantity = DataCleaner.clean_float_value(data_dict.get('batch_quantity')),
            batch_number = DataCleaner.clean_str_value(data_dict.get('batch_number')),
            device_batch_id = int(data_dict.get('device_batch_id', 0)),
            device_name = DataCleaner.clean_str_value(data_dict.get('device_name', '')),
            device_id = int(data_dict.get('device_id', 0)),
            device_batch_start_time = DataCleaner.clean_datetime_value(data_dict.get('device_batch_start_time')),
            device_batch_end_time = DataCleaner.clean_datetime_value(data_dict.get('device_batch_end_time')),

            # 一次煎煮设定参数
            p1_up_temp_set = DataCleaner.clean_float_value(data_dict.get('p1_up_temp_set')),
            p1_up_temp_press_set = DataCleaner.clean_float_value(data_dict.get('p1_up_temp_press_set')),
            p1_hold_temp_set = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_set')),
            p1_hold_temp_press_set = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_press_set')),
            p1_hold_temp_time_set = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_time_set')),
            p1_solvent_num_set = DataCleaner.clean_float_value(data_dict.get('p1_solvent_num_set')),
            # 一次煎煮升温
            p1_up_temp_start_time = DataCleaner.clean_datetime_value(data_dict.get('p1_up_temp_start_time')),
            p1_up_temp_end_time = DataCleaner.clean_datetime_value(data_dict.get('p1_up_temp_end_time')),
            p1_up_temp_min_press = DataCleaner.clean_float_value(data_dict.get('p1_up_temp_min_press')),
            p1_up_temp_max_press = DataCleaner.clean_float_value(data_dict.get('p1_up_temp_max_press')),
            # 一次煎煮保温
            p1_hold_temp_start_time = DataCleaner.clean_datetime_value(data_dict.get('p1_hold_temp_start_time')),
            p1_hold_temp_end_time = DataCleaner.clean_datetime_value(data_dict.get('p1_hold_temp_end_time')),
            p1_hold_temp_min_press = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_min_press')),
            p1_hold_temp_max_press = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_max_press')),
            p1_hold_temp_time = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_time')),
            p1_hold_temp_min_temp = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_min_temp')),
            p1_hold_temp_max_temp = DataCleaner.clean_float_value(data_dict.get('p1_hold_temp_max_temp')),
            # 一次煎煮溶媒和出液
            p1_solvent_num = DataCleaner.clean_float_value(data_dict.get('p1_solvent_num')),
            p1_out_num = DataCleaner.clean_float_value(data_dict.get('p1_out_num')),
            # 一次煎煮整体时间
            p1_start_time = DataCleaner.clean_datetime_value(data_dict.get('p1_start_time')),
            p1_end_time = DataCleaner.clean_datetime_value(data_dict.get('p1_end_time'))
        )
    
# 双效浓缩器数据清洗
class SXDataCleaner:
    @staticmethod
    def clean_dataframe(raw_df: pd.DataFrame) -> SXReportData:
        if raw_df.empty:
            raise ValueError('双效浓缩器报表数据为空！')
        data_dict = raw_df.iloc[0].to_dict()
        # 添加双效浓缩器报表数据
        return SXReportData()

class DataCleanerFactory:
    CLEANER_MAPPING: Dict[str, type] = {
        'T_TQ_Batch_Archive': TQDataCleaner,
        'T_SX_Batch_Archive': SXDataCleaner
    }
    REPORTDATA_MAPPING: Dict[str, type] = {
        'T_TQ_Batch_Archive': TQReportData,
        'T_SX_Batch_Archive': SXReportData
    }

    @classmethod
    def get_cleaner(cls, table_name: str) -> type:
        cleaner = cls.CLEANER_MAPPING.get(table_name)
        if not cleaner:
            raise ValueError(f"不支持的报表类型: {table_name}")
        return cleaner
    
    @classmethod
    def clean_dataframe(cls, table_name: str, raw_df: pd.DataFrame) -> type:
        cleaner = cls.get_cleaner(table_name)
        return cleaner.clean_dataframe(raw_df)

class TQReportTemplateProcessor:
    @staticmethod
    def create_report_template_dataframe(data: TQReportData) -> dict[str, Any]:
        if not isinstance(data, TQReportData):
            raise ValueError("设备类型不匹配，必须是提取罐类型")
        header_rows = [
            {
                'A': '品名',
                'B': data.product_name,
                'C': '批量',
                'D': data.batch_quantity,
                'E': '批号',
                'F': data.batch_number,
            },
            {
                'A': '设备名称',
                'B': data.device_name,
                'C': '设备编号',
                'D': data.device_id
            },
            {
                'A': '开始时间',
                'B': data.device_batch_start_time,
                'C': '结束时间',
                'D': data.device_batch_end_time
            }
        ]
        p1_set_rows = [
            {
                'A': '升温压力设定',
                'B': data.p1_up_temp_press_set,
                'C': '保温压力设定',
                'D': data.p1_hold_temp_press_set,
                'E': '加溶媒量',
                'F': data.p1_solvent_num_set
            },
            {
                'A': '升温温度设定',
                'B': data.p1_up_temp_set,
                'C': '保温温度设定',
                'D': data.p1_hold_temp_set,
                'E': '保温时间设定',
                'F': data.p1_hold_temp_time_set
            }
        ]
        p1_record_rows = [
            {
                'A': '升温开始时间',
                'B': data.p1_up_temp_start_time,
                'C': '升温结束时间',
                'D': data.p1_up_temp_end_time,
                'E': '加溶媒量',
                'F': data.p1_solvent_num
            },
            {
                'A': '保温开始时间',
                'B': data.p1_hold_temp_start_time,
                'C': '保温结束时间',
                'D': data.p1_hold_temp_end_time,
                'E': '保温时间',
                'F': data.p1_hold_temp_time
            },
            {
                'A': '升温最低压力',
                'B': data.p1_up_temp_min_press,
                'C': '保温最低压力',
                'D': data.p1_hold_temp_min_press,
                'E': '保温最低温度',
                'F': data.p1_hold_temp_min_temp
            },
            {
                'A': '升温最高压力',
                'B': data.p1_up_temp_max_press,
                'C': '保温最高压力',
                'D': data.p1_hold_temp_max_press,
                'E': '保温最高温度',
                'F': data.p1_hold_temp_max_temp
            },
            {
                'A': '出液量',
                'B': data.p1_out_num
            }
        ]
        footer_rows = [
            {
                'A': '操作人',
                'B': '',
                'C': '复核人',
                'D': '',
                'E': '报表生成时间',
                'F': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        # 返回标准化的数据结构
        template_df = {
            'sections': [
                {
                    'title': '基本信息',
                    'type': 'info',
                    'data': pd.DataFrame(header_rows).fillna('').astype(str)
                },
                {
                    'title': '一次参数设置',
                    'type': 'parameters',
                    'data': pd.DataFrame(p1_set_rows).fillna('').astype(str)
                },
                {
                    'title': '一次煎煮记录',
                    'type': 'records',
                    'data': pd.DataFrame(p1_record_rows).fillna('').astype(str)
                },
                {
                    'title': '其他信息',
                    'type': 'summary',
                    'data': pd.DataFrame(footer_rows).fillna('').astype(str)
                }
            ]
        }
        return template_df

class SXReportTemplateProcessor:
    @staticmethod
    def create_report_template_dataframe(data: SXReportData) -> dict[str, pd.DataFrame]:
        if not isinstance(data, SXReportData):
            raise ValueError("数据类型不匹配，必须是双效浓缩器报表")
        rows = [
            {
                # 双效浓缩器报表内容
            }
        ]
        template_df = {}
        return template_df

class ReportTemplateProcessor:
    PROCESSOR_MAPPING: dict[str, type] = {
        "T_TQ_Batch_Archive": TQReportTemplateProcessor,
        "T_SX_Batch_Archive": SXReportTemplateProcessor
    }

    @classmethod
    def convert_to_template_df(cls, cleaned_data, table_name: str) -> dict[str, Any]:
            processor = cls.PROCESSOR_MAPPING.get(table_name)
            if processor:
                return processor.create_report_template_dataframe(cleaned_data)
            else:
                raise ValueError(f"不支持的报表类型: {table_name}")


# 工厂方法，供外部调用
def get_report_template_dataframe(table_name: str, raw_df: pd.DataFrame) -> dict[str, Any]:
    cleaned_data = DataCleanerFactory.clean_dataframe(table_name, raw_df)
    template_df = ReportTemplateProcessor.convert_to_template_df(cleaned_data, table_name)
    return template_df

def get_formatted_datetime_df(df: pd.DataFrame) -> pd.DataFrame:
    return DataCleaner.format_datetime_value(df)
