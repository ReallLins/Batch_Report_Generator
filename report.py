import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from typing import Dict, Any, Optional
from datetime import datetime


class BaseReport:
    def __init__(self, column_num: int):
        self.workbook_name = '' # 文件名
        self.worksheet_name = '' # 工作表名
        self.file_path = f'{self.workbook_name}.xlsx'  # 默认文件路径
        self.color = '000000' # 字体、边框颜色
        self.name = '宋体'
        self.title = '' # 报表标题
        # 标题样式
        self.title_font = Font(name=self.name, size=18, bold=True, color=self.color)
        # 表头及小标题样式
        self.header_font = Font(name=self.name, size=11, bold=True, color=self.color)
        # 数据样式
        self.data_font = Font(name=self.name, size=11, bold=False, color=self.color)
        # 对齐
        self.center_align = Alignment(horizontal='center', vertical='center')
        # 边框
        self.border = Border(
            left=Side(style='thin', color=self.color),
            right=Side(style='thin', color=self.color),
            top=Side(style='thin', color=self.color),
            bottom=Side(style='thin', color=self.color)
        )
        self.column_num = column_num
        # self.workbook = Workbook()
        # self.worksheet = self.workbook.active
        # 添加填充色
        self.title_fill = PatternFill(fill_type=None)
        self.header_fill = PatternFill(fill_type=None)

    def _create_workbook(self) -> tuple[Workbook, Worksheet]:
        workbook = Workbook()
        worksheet = workbook.active
        # 这句其实没啥用，主要是为了消除类型注解报错
        if worksheet is None:
            worksheet = workbook.create_sheet()
        return (workbook, worksheet)

    # 添加报表标题
    def _add_title(self, ws: Worksheet) -> int:
        ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=self.column_num)
        title_cell: Cell = ws['A1']
        title_cell.value = self.title
        title_cell.font = self.title_font
        title_cell.fill = self.title_fill
        title_cell.border = self.border
        title_cell.alignment = self.center_align
        return 2  # 返回下一行的位置

    # 添加小标题
    def _add_header_title(self, ws: Worksheet, header_title: str, start_row: int) -> int:
        current_row = start_row
        ws.merge_cells(start_row=current_row, end_row=current_row, start_column=1, end_column=self.column_num)
        header_cell: Cell = ws[f'A{current_row}']
        header_cell.value = header_title
        header_cell.font = self.header_font
        header_cell.fill = self.header_fill
        header_cell.border = self.border
        header_cell.alignment = self.center_align
        return current_row + 1

    # 添加表头尾内容，注意这里直接用dataframe批量写入了，没做任何判断
    def _add_header_footer_info(self, ws: Worksheet, header_footer_data: pd.DataFrame, start_row: int) -> int:
        current_row = start_row
        if header_footer_data is None or header_footer_data.empty:
            return current_row
        rows_cnt, cols_cnt = header_footer_data.shape
        rows = dataframe_to_rows(header_footer_data, index=False, header=True)
        for row in rows:
            ws.append(row)
        last_row = current_row + rows_cnt - 1
        for row in ws.iter_rows(min_row=current_row, max_row=last_row, min_col=1, max_col=cols_cnt):
            for cell in row:
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.border = self.border
                cell.alignment = self.center_align
        return last_row + 1
    
    # 添加报表数据
    def _add_data(self, ws: Worksheet, data: pd.DataFrame, start_row: int) -> int:
        current_row = start_row
        if data is None or data.empty:
            return current_row
        rows_cnt, cols_cnt = data.shape
        rows = dataframe_to_rows(data, index=False, header=False)
        for row in rows:
            ws.append(row)
        last_row = current_row + rows_cnt - 1
        for row in ws.iter_rows(min_row=current_row, max_row=last_row, min_col=1, max_col=cols_cnt):
            for cell in row:
                cell.font = self.data_font
                cell.border = self.border
                cell.alignment = self.center_align
        return last_row + 1


class TQReportGenerator(BaseReport):
    def __init__(self):
        self.column_num = 8

    def generate_report(self, device_name: str, report_data: dict[str, list[pd.DataFrame]]) -> bytes:
        wb, ws = self._create_workbook()
        self.title = f"提取车间自控报表--{device_name}"
        # 报表标题
        current_row = self._add_title(ws)
        # header_info
        header_info = report_data['header'][0]
        current_row = self._add_header_footer_info(ws, header_info, current_row)
        # main_info
        main_info = report_data['main']
        header_title = ['一次参数设置', '一次煎煮记录']
        for title, data in zip(header_title, main_info):
            current_row = self._add_header_title(ws, title, current_row)
            current_row = self._add_data(ws, data, current_row)
        # footer_info
        footer_info = report_data['footer'][0]
        self._add_header_footer_info(ws, footer_info, current_row)
        
        # # 调整列宽
        # try:
        #     # 简化的列宽调整
        #     for i, col in enumerate(ws.columns, 1):
        #         max_length = 0
        #         column_letter = chr(64 + i)  # 简单地使用 A, B, C...
        #         for cell in col:
        #             try:
        #                 if cell.value and len(str(cell.value)) > max_length:
        #                     max_length = len(str(cell.value))
        #             except:
        #                 pass
        #         adjusted_width = min(max_length + 2, 50)
        #         ws.column_dimensions[column_letter].width = adjusted_width
        # except Exception:
        #     # 如果调整列宽失败，忽略错误
        #     pass
        
        # 保存到内存
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer.read()

class ReportGeneratorFactory:
    GENERATOR_MAPPING: dict[str, type] = {
        "T_TQ_Batch_Archive": TQReportGenerator
    }

    @classmethod
    def create_report_generator(cls, table_name: str) -> type:
        generator_class = cls.GENERATOR_MAPPING.get(table_name)
        if generator_class:
            return generator_class()
        else:
            raise ValueError(f"不支持的报表类型: {table_name}")

# 工厂方法，供外部调用
def get_report(report_data, table_name: str, device_name: str) -> bytes:
    generator = ReportGeneratorFactory.create_report_generator(table_name)
    report = generator.generate_report(device_name, report_data)
    return report
