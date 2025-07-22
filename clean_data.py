import pandas as pd
from dataclasses import dataclass
from typing import Optional, Dict, Any, Protocol, Union, runtime_checkable
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
    device_batch_start_time: Optional[datetime]
    device_batch_end_time: Optional[datetime]

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
    p1_up_temp_start_time: Optional[datetime]
    p1_up_temp_end_time: Optional[datetime]
    p1_up_temp_min_press: Optional[float]
    p1_up_temp_max_press: Optional[float]
    # 一次煎煮保温
    p1_hold_temp_start_time: Optional[datetime]
    p1_hold_temp_end_time: Optional[datetime]
    p1_hold_temp_min_press: Optional[float]
    p1_hold_temp_max_press: Optional[float]
    p1_hold_temp_time: Optional[float]
    p1_hold_temp_min_temp: Optional[float]
    p1_hold_temp_max_temp: Optional[float]
    # 一次煎煮溶媒和出液
    p1_solvent_num: Optional[float]
    p1_out_num: Optional[float]
    # 一次煎煮整体时间
    p1_start_time: Optional[datetime]
    p1_end_time: Optional[datetime]

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
    device_batch_start_time: Optional[datetime] = None
    device_batch_end_time: Optional[datetime] = None

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
    p1_up_temp_start_time: Optional[datetime] = None
    p1_up_temp_end_time: Optional[datetime] = None
    p1_up_temp_min_press: Optional[float] = 0.0
    p1_up_temp_max_press: Optional[float] = 0.0
    # 一次煎煮保温
    p1_hold_temp_start_time: Optional[datetime] = None
    p1_hold_temp_end_time: Optional[datetime] = None
    p1_hold_temp_min_press: Optional[float] = 0.0
    p1_hold_temp_max_press: Optional[float] = 0.0
    p1_hold_temp_time: Optional[float] = 0.0
    p1_hold_temp_min_temp: Optional[float] = 0.0
    p1_hold_temp_max_temp: Optional[float] = 0.0
    # 一次煎煮溶媒和出液
    p1_solvent_num: Optional[float] = 0.0
    p1_out_num: Optional[float] = 0.0
    # 一次煎煮整体时间
    p1_start_time: Optional[datetime] = None
    p1_end_time: Optional[datetime] = None

@dataclass
class SXReportData(BaseReportData, SXReportDataProtocol):
    # 双效浓缩器特有参数可以在这里定义
    pass

# 基础数据清洗工具
class DataCleaner:
    @staticmethod
    def clean_float_value(value: Any) -> Optional[float]:
        # 清洗数字类型数据
        if value is None or pd.isna(value):
            return None
        
        try:
            if isinstance(value, str):
                value = value.strip()
                if value == '' or value.lower() in ['null', 'none', 'n/a', 'nan']:
                    return None
                # 移除千位分隔符
                value = value.replace(',', '')
            
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def clean_datetime_value(value: Any) -> Optional[datetime]:
        # 清洗日期时间数据
        if value is None or pd.isna(value):
            return None
        
        try:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, str):
                value = value.strip()
                if value == '' or value.lower() in ['null', 'none', 'n/a']:
                    return None
                
                # 尝试多种日期格式
                date_formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M:%S.%f',
                    '%Y-%m-%d',
                    '%Y/%m/%d %H:%M:%S',
                    '%Y/%m/%d'
                ]
                
                for fmt in date_formats:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
            return None
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def clean_str_value(value: Any) -> Optional[str]:
        # 清洗字符串数据
        if value is None or pd.isna(value):
            return None
        
        try:
            str_value = str(value).strip()
            if str_value == '' or str_value.lower() in ['null', 'none', 'n/a', 'nan']:
                return None
            return str_value
        except:
            return None

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
    def create_report_template_dataframe(data: TQReportData) -> dict[str, pd.DataFrame]:
        if not isinstance(data, TQReportData):
            raise ValueError("数据类型不匹配，必须是提取罐报表")
        header_rows = [
            {
                'col1': '品名',
                'col2': data.product_name,
                'col3': '批量',
                'col4': data.batch_quantity,
                'col5': '批号',
                'col6': data.batch_number,
            },
            {
                'col1': '设备名称',
                'col2': data.device_name,
                'col3': '设备编号',
                'col4': data.device_id,
                'col5': '开始时间',
                'col6': data.device_batch_start_time,
                'col7': '结束时间',
                'col8': data.device_batch_end_time
            }
        ]
        p1_set_rows = [
            {
                'col1': '升温压力设定',
                'col2': data.p1_up_temp_press_set,
                'col3': '保温压力设定',
                'col4': data.p1_hold_temp_press_set,
                'col5': '加溶媒量',
                'col6': data.p1_solvent_num_set
            },
            {
                'col1': '升温温度设定',
                'col2': data.p1_up_temp_set,
                'col3': '保温温度设定',
                'col4': data.p1_hold_temp_set,
                'col5': '保温时间设定',
                'col6': data.p1_hold_temp_time_set
            }
        ]
        p1_record_rows = [
            {
                'col1': '升温开始时间',
                'col2': data.p1_up_temp_start_time,
                'col3': '升温结束时间',
                'col4': data.p1_up_temp_end_time,
                'col5': '加溶媒量',
                'col6': data.p1_solvent_num
            },
            {
                'col1': '保温开始时间',
                'col2': data.p1_hold_temp_start_time,
                'col3': '保温结束时间',
                'col4': data.p1_hold_temp_end_time,
                'col5': '保温时间',
                'col6': data.p1_hold_temp_time
            },
            {
                'col1': '升温最低压力',
                'col2': data.p1_up_temp_min_press,
                'col3': '保温最低压力',
                'col4': data.p1_hold_temp_min_press,
                'col5': '保温最低温度',
                'col6': data.p1_hold_temp_min_temp
            },
            {
                'col1': '升温最高压力',
                'col2': data.p1_up_temp_max_press,
                'col3': '保温最高压力',
                'col4': data.p1_hold_temp_max_press,
                'col5': '保温最高温度',
                'col6': data.p1_hold_temp_max_temp
            },
            {
                'col1': '出液量',
                'col2': data.p1_out_num
            }
        ]
        footer_rows = [
            {
                'col1': '操作人',
                'col2': '',
                'col3': '复核人',
                'col4': '',
                'col5': '报表生成时间',
                'col6': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        main_rows = [p1_set_rows, p1_record_rows]

        template_df = {}
        template_df['header'] = [pd.DataFrame(header_rows)]
        template_df['footer'] = [pd.DataFrame(footer_rows)]
        template_df['main'] = [pd.DataFrame(rows) for rows in main_rows]
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
    def convert_to_template_df(cls, cleaned_data, table_name: str) -> dict[str, pd.DataFrame]:
            processor = cls.PROCESSOR_MAPPING.get(table_name)
            if processor:
                return processor.create_report_template_dataframe(cleaned_data)
            else:
                raise ValueError(f"不支持的报表类型: {table_name}")


# 工厂方法，供外部调用
def get_report_template_dataframe(table_name: str, raw_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    cleaned_data = DataCleanerFactory.clean_dataframe(table_name, raw_df)
    template_df = ReportTemplateProcessor.convert_to_template_df(cleaned_data, table_name)
    return template_df
