#!/usr/bin/env python3
"""
系统测试脚本
验证批次报表生成器的基本功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    try:
        from models import T_Batch, T_Device_Info, T_TQ_Batch_Archive, T_Device_Batch
        from report import generate_tq_report, ReportDataProtocol
        from database import get_engine
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_report_generation():
    """测试报表生成功能"""
    try:
        from dataclasses import dataclass
        from datetime import datetime
        from typing import Optional
        from report import generate_tq_report
        
        @dataclass
        class TestReportData:
            device_id: int = 1
            device_name: Optional[str] = "测试提取罐"
            product_name: Optional[str] = "测试产品"
            batch_number: str = "TEST001"
            # 工艺参数
            p1_up_temp_set: Optional[float] = 85.0
            p1_up_temp_press_set: Optional[float] = 0.5
            p1_hold_temp_set: Optional[float] = 80.0
            p1_hold_temp_press_set: Optional[float] = 0.3
            p1_solvent_num_set: Optional[float] = 1000.0
            # 生产过程
            p1_up_temp_start_time: Optional[datetime] = datetime.now()
            p1_up_temp_end_time: Optional[datetime] = datetime.now()
            p1_up_temp_min_press: Optional[float] = 0.2
            p1_up_temp_max_press: Optional[float] = 0.6
            p1_hold_temp_start_time: Optional[datetime] = datetime.now()
            p1_hold_time_end_tme: Optional[datetime] = datetime.now()
            p1_hold_temp_min_press: Optional[float] = 0.2
            p1_hold_temp_max_press: Optional[float] = 0.4
            # 生产结果
            p1_solvent_num: Optional[float] = 950.0
            p1_out_num: Optional[float] = 900.0
            p1_hold_temp_min_temp: Optional[float] = 78.0
            p1_hold_temp_max_temp: Optional[float] = 82.0
        
        test_data = TestReportData()
        excel_data = generate_tq_report(test_data)
        
        if excel_data and len(excel_data) > 0:
            print("✅ 报表生成测试成功")
            print(f"   生成的 Excel 文件大小: {len(excel_data)} 字节")
            return True
        else:
            print("❌ 报表生成失败：生成的数据为空")
            return False
    except Exception as e:
        print(f"❌ 报表生成测试失败: {e}")
        return False

def test_models():
    """测试模型定义"""
    try:
        from models import T_TQ_Batch_Archive, T_Device_Batch, T_Batch, T_Device_Info
        from decimal import Decimal
        
        # 创建测试实例
        batch = T_Batch(
            batch_number="TEST001",
            product_name="测试产品"
        )
        
        device_info = T_Device_Info(
            device_id=1,
            device_type_id=1,
            device_name="测试提取罐",
            batch_number="TEST001"
        )
        
        device_batch = T_Device_Batch(
            device_batch_id=1,
            device_id=1,
            batch_number="TEST001"
        )
        
        archive = T_TQ_Batch_Archive(
            device_batch_id=1,
            device_id=1,
            p1_up_temp_set=Decimal('85.0')
        )
        
        print("✅ 模型定义测试成功")
        return True
    except Exception as e:
        print(f"❌ 模型定义测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始批次报表生成器系统测试")
    print("-" * 50)
    
    tests = [
        ("导入测试", test_imports),
        ("模型测试", test_models),
        ("报表生成测试", test_report_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   详细信息: {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！系统就绪。")
        return True
    else:
        print("⚠️  部分测试失败，请检查系统配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
