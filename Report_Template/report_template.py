TQ_REPORT_TEMPLATE = {
    "title": "提取车间自控报表-提取罐1",
    "header": {
        "基本信息":[
            {
                'A': '品名',
                'B': "product_name",
                'C': '批量',
                'D': "batch_quantity",
                'E': '批号',
                'F': "batch_number",
            },
            {
                'A': '设备名称',
                'B': "device_name",
                'C': '设备编号',
                'D': "device_id"
            },
            {
                'A': '开始时间',
                'B': "device_batch_start_time",
                'C': '结束时间',
                'D': "device_batch_end_time"
            }
        ]
    },
    "body": {
        "一次参数设置": [
            {
                'A': '升温压力设定',
                'B': "p1_up_temp_press_set",
                'C': '保温压力设定',
                'D': "p1_hold_temp_press_set",
                'E': '加溶媒量',
                'F': "p1_solvent_num_set"
            },
            {
                'A': '升温温度设定',
                'B': "p1_up_temp_set",
                'C': '保温温度设定',
                'D': "p1_hold_temp_set",
                'E': '保温时间设定',
                'F': "p1_hold_temp_time_set"
            }
        ],
        "一次煎煮记录": [
            {
                'A': '升温开始时间',
                'B': "p1_up_temp_start_time",
                'C': '升温结束时间',
                'D': "p1_up_temp_end_time",
                'E': '加溶媒量',
                'F': "p1_solvent_num"
            },
            {
                'A': '保温开始时间',
                'B': "p1_hold_temp_start_time",
                'C': '保温结束时间',
                'D': "p1_hold_temp_end_time",
                'E': '保温时间',
                'F': "p1_hold_temp_time"
            },
            {
                'A': '升温最低压力',
                'B': "p1_up_temp_min_press",
                'C': '保温最低压力',
                'D': "p1_hold_temp_min_press",
                'E': '保温最低温度',
                'F': "p1_hold_temp_min_temp"
            },
            {
                'A': '升温最高压力',
                'B': "p1_up_temp_max_press",
                'C': '保温最高压力',
                'D': "p1_hold_temp_max_press",
                'E': '保温最高温度',
                'F': "p1_hold_temp_max_temp"
            },
            {
                'A': '出液量',
                'B': "p1_out_num"
            }
        ]
    },
    "footer": {
        "其他信息": [
            {
                'A': '操作人',
                'B': '',
                'C': '复核人',
                'D': '',
                'E': '报表生成时间',
                'F': "datetime.now().strftime('%Y-%m-%d %H:%M:%S')"
            }
        ]
    }
}