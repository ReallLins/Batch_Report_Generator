import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell
from io import BytesIO
from typing import Dict, Any, Optional, Protocol
from datetime import datetime


class ReportDataProtocol(Protocol):
    """定义报表数据的协议，用于类型提示"""
    device_id: int
    device_name: Optional[str]
    product_name: Optional[str]
    batch_number: str
    # 工艺参数
    p1_up_temp_set: Optional[float]
    p1_up_temp_press_set: Optional[float]
    p1_hold_temp_set: Optional[float]
    p1_hold_temp_press_set: Optional[float]
    p1_solvent_num_set: Optional[float]
    # 生产过程
    p1_up_temp_start_time: Optional[datetime]
    p1_up_temp_end_time: Optional[datetime]
    p1_up_temp_min_press: Optional[float]
    p1_up_temp_max_press: Optional[float]
    p1_hold_temp_start_time: Optional[datetime]
    p1_hold_time_end_tme: Optional[datetime]
    p1_hold_temp_min_press: Optional[float]
    p1_hold_temp_max_press: Optional[float]
    # 生产结果
    p1_solvent_num: Optional[float]
    p1_out_num: Optional[float]
    p1_hold_temp_min_temp: Optional[float]
    p1_hold_temp_max_temp: Optional[float]


class Report_Generator:
    def __init__(self):
        self.workbook_name = '' # 文件名
        self.worksheet_name = '' # 工作表名
        self.file_path = f'{self.workbook_name}.xlsx'  # 默认文件路径
        self.color = '000000' # 字体、边框颜色
        self.name = '宋体'
        self.title = '' # 报表标题
        # 字体样式
        self.title_font = Font(name=self.name, size=18, bold=True, color=self.color)
        self.header_font = Font(name=self.name, size=11, bold=True, color=self.color)
        self.data_font = Font(name=self.name, size=11, bold=False, color=self.color)
        self.center_align = Alignment(horizontal='center', vertical='center')
        self.border = Border(
            left=Side(style='thin', color=self.color),
            right=Side(style='thin', color=self.color),
            top=Side(style='thin', color=self.color),
            bottom=Side(style='thin', color=self.color)
        )
        self.column_num = 0
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        # 添加表头填充色
        self.header_fill = PatternFill(start_color='E6E6E6', end_color='E6E6E6', fill_type='solid')
    
    def _add_title(self, ws: Worksheet, title: str, column_count: int = 5) -> int:
        """添加报表标题"""
        ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=column_count)
        title_cell = ws['A1']
        title_cell.value = title
        title_cell.font = self.title_font
        title_cell.alignment = self.center_align
        return 3  # 返回下一行的位置

    def _add_info_section(self, ws: Worksheet, info_data: Dict[str, Any], start_row: int) -> int:
        """添加信息段落"""
        current_row = start_row
        
        # 基本信息标题
        ws[f'A{current_row}'] = "基本信息"
        ws[f'A{current_row}'].font = self.header_font
        current_row += 1
        
        # 信息内容
        col = 0
        for key, value in info_data.items():
            if col % 2 == 0:  # 新行
                current_row += 1
                ws.cell(row=current_row, column=1, value=f"{key}:")
                ws.cell(row=current_row, column=2, value=str(value or ""))
            else:  # 同行右侧
                ws.cell(row=current_row, column=4, value=f"{key}:")
                ws.cell(row=current_row, column=5, value=str(value or ""))
            col += 1
        
        return current_row + 2
    
    def _add_data_table(self, ws: Worksheet, headers: list, data: list, start_row: int) -> int:
        """添加数据表格"""
        current_row = start_row
        
        # 添加表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=current_row, column=col, value=header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = self.center_align
            cell.border = self.border
        
        current_row += 1
        
        # 添加数据
        for row_data in data:
            for col, value in enumerate(row_data, 1):
                cell = ws.cell(row=current_row, column=col, value=value)
                cell.font = self.data_font
                cell.border = self.border
                if isinstance(value, (int, float)):
                    cell.alignment = Alignment(horizontal='right', vertical='center')
                else:
                    cell.alignment = Alignment(horizontal='left', vertical='center')
            current_row += 1
        
        return current_row + 1


class TQ_Report_Generator(Report_Generator):
    
    def generate_report(self, report_data: ReportDataProtocol) -> bytes:
        """生成提取罐报表 - 接受任何包含必要属性的对象"""
        wb = Workbook()
        ws = wb.active
        if ws is None:
            raise ValueError("无法创建工作表")
        
        ws.title = "提取罐生产报表"
        
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