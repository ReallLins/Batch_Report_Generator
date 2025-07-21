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
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        # 添加填充色
        self.title_fill = PatternFill(fill_type=None)
        self.header_fill = PatternFill(fill_type=None)
    
    # 添加报表标题
    def _add_title(self, ws: Worksheet, title: str) -> int:
        ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=self.column_num)
        title_cell = ws['A1']
        title_cell.value = title
        title_cell.font = self.title_font
        title_cell.fill = self.title_fill
        title_cell.border = self.border
        title_cell.alignment = self.center_align
        return 2  # 返回下一行的位置

    # 添加小标题
    def _add_header_title(self, ws: Worksheet, header_title: str, start_row: int) -> int:
        current_row = start_row
        ws.merge_cells(start_row=current_row, end_row=current_row, start_column=1, end_column=self.column_num)
        header_cell = ws[f'A{current_row}']
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
    def generate_report(self, device_name: str, report_data: list[pd.DataFrame]) -> bytes:
        wb = Workbook()
        ws = wb.active
        self.title = f"提取车间自控报表--{device_name}"
        
        # 报表标题
        current_row = self._add_title(ws, "提取罐生产报表")
        
        # 基本信息
        info_data = {
            "产品名称": getattr(report_data, 'product_name', None),
            "批次号": getattr(report_data, 'batch_number', None),
            "设备名称": getattr(report_data, 'device_name', None),
            "设备ID": getattr(report_data, 'device_id', None),
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        current_row = self._add_info_section(ws, info_data, current_row)
        
        # 工艺参数
        ws[f'A{current_row}'] = "工艺参数"
        ws[f'A{current_row}'].font = self.header_font
        current_row += 1
        
        process_headers = ["参数名称", "设定值", "单位", "备注"]
        process_data = [
            ["升温设定温度", getattr(report_data, 'p1_up_temp_set', None), "℃", ""],
            ["升温设定压力", getattr(report_data, 'p1_up_temp_press_set', None), "Bar", ""],
            ["保温设定温度", getattr(report_data, 'p1_hold_temp_set', None), "℃", ""],
            ["保温设定压力", getattr(report_data, 'p1_hold_temp_press_set', None), "Bar", ""],
            ["溶媒设定量", getattr(report_data, 'p1_solvent_num_set', None), "L", ""],
        ]
        current_row = self._add_data_table(ws, process_headers, process_data, current_row)
        
        # 生产过程
        ws[f'A{current_row}'] = "生产过程"
        ws[f'A{current_row}'].font = self.header_font
        current_row += 1
        
        process_headers = ["阶段", "开始时间", "结束时间", "最小压力", "最大压力", "备注"]
        process_data = [
            ["升温", getattr(report_data, 'p1_up_temp_start_time', None), 
             getattr(report_data, 'p1_up_temp_end_time', None),
             getattr(report_data, 'p1_up_temp_min_press', None), 
             getattr(report_data, 'p1_up_temp_max_press', None), ""],
            ["保温", getattr(report_data, 'p1_hold_temp_start_time', None), 
             getattr(report_data, 'p1_hold_time_end_tme', None),
             getattr(report_data, 'p1_hold_temp_min_press', None), 
             getattr(report_data, 'p1_hold_temp_max_press', None), ""],
        ]
        current_row = self._add_data_table(ws, process_headers, process_data, current_row)
        
        # 生产结果
        ws[f'A{current_row}'] = "生产结果"
        ws[f'A{current_row}'].font = self.header_font
        current_row += 1
        
        result_headers = ["项目", "数值", "单位", "备注"]
        result_data = [
            ["实际溶媒量", getattr(report_data, 'p1_solvent_num', None), "L", ""],
            ["实际出液量", getattr(report_data, 'p1_out_num', None), "L", ""],
            ["保温最低温度", getattr(report_data, 'p1_hold_temp_min_temp', None), "℃", ""],
            ["保温最高温度", getattr(report_data, 'p1_hold_temp_max_temp', None), "℃", ""],
        ]
        current_row = self._add_data_table(ws, result_headers, result_data, current_row)
        
        # 调整列宽
        try:
            # 简化的列宽调整
            for i, col in enumerate(ws.columns, 1):
                max_length = 0
                column_letter = chr(64 + i)  # 简单地使用 A, B, C...
                for cell in col:
                    try:
                        if cell.value and len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
        except Exception:
            # 如果调整列宽失败，忽略错误
            pass
        
        # 保存到内存
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer.read()


def Create_Report_Generator(device_type: str) -> Optional[Report_Generator]:
    """根据设备类型创建对应的报表生成器"""
    generators = {
        "TQ": TQ_Report_Generator,
        # 未来可以添加更多设备类型
        # "DX": DXReportGenerator,
        # "SX": SXReportGenerator,
    }
    
    generator_class = generators.get(device_type.upper())
    if generator_class:
        return generator_class()
    return None


# 便捷函数
def generate_tq_report(report_data: ReportDataProtocol) -> bytes:
    """生成提取罐报表的便捷函数"""
    generator = TQ_Report_Generator()
    return generator.generate_report(report_data)