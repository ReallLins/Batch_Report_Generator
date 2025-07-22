from get_data import get_device_info, get_report_data, get_device_type, get_device_list
from database_config import DatabaseConfig
import pandas as pd
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows


database_config = DatabaseConfig("124.71.179.195", "1433", "Kangde_Test", "sa", "Admin_1")

# device_info = get_device_info(database_config, 1)
# print(device_info) if device_info is not None else print("获取设备信息失败")

# report_data = get_report_data(database_config, "TZ25071401", 1)
# print(report_data) if report_data is not None else print("获取报表数据失败")

# device_type = get_device_type(database_config)
# print(device_type) if device_type is not None else print("获取设备类型失败")

# device_list = get_device_list(database_config, 3)
# print(device_list) if device_list is not None else print("获取设备列表失败")

rows1 = [
    {
        'col1': '品名',
        'col2': '红花',
        'col3': '批号',
        'col4': 'TZ25071801',
        'col5': '批量',
        'col6': '100',
    },
    {
        'col1': '设备名称',
        'col2': '1#提取罐',
        'col3': '设备编号',
        'col4': '1',
        'col5': '开始时间',
        'col6': '2025-07-18 10:00:00',
        'col7': '结束时间',
        'col8': '2025-07-18 12:00:00'
    }
]
rows2 = [
    {
        'col1': '升温压力设定',
        'col2': 1.0,
        'col3': '保温压力设定',
        'col4': 1.5,
        'col5': '加溶媒量',
        'col6': 100.0
    },
    {
        'col1': '升温温度设定',
        'col2': 80.0,
        'col3': '保温温度设定',
        'col4': 90.0,
        'col5': '保温时间设定',
        'col6': 120.0
    }
]


