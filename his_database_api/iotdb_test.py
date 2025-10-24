import numpy as np
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb_config import get_iotdb_config
import get_iotdb_data
import atexit
import pandas as pd
import time


new_iotdb = get_iotdb_config()
session_pool = new_iotdb.create_session_pool()

device_id = "root.test_group.tq_tank_1"
measurements = ["temp", "press"]
data_types = [TSDataType.FLOAT, TSDataType.FLOAT]
encodings = [TSEncoding.PLAIN, TSEncoding.PLAIN]
compressors = [Compressor.SNAPPY, Compressor.SNAPPY]
insert_data_list = ["root.test_group.tq_tank_1.temp", "root.test_group.tq_tank_1.press"]
query_data_list = ["tq_tank_1.temp", "tq_tank_1.press"]
insert_times = {
    "start_time": "2025-10-22 08:00:00",
    "end_time": "2025-10-22 20:00:00",
    "interval": 60
}

query_times = {
    "start_time": "2025-10-22 12:00:00",
    "end_time": "2025-10-22 18:00:00",
    "interval": 1800
}
# timestamps = pd.date_range(
#     start=times["start_time"],
#     end=times["end_time"],
#     freq=f"{times['interval']}s",
#     tz="UTC+08:00"
# )
# np_timestamps = (timestamps.values.astype(np.int64) // 10**6).astype(TSDataType.INT64.np_dtype())
# nums = len(np_timestamps)
# temp_values = [30.7 + v * 0.03 for v in range(nums)]
# press_values = [100.3 + v * 0.07 for v in range(nums)]
# np_values = [
#     np.array(temp_values, TSDataType.FLOAT.np_dtype()),
#     np.array(press_values, TSDataType.FLOAT.np_dtype())
# ]
# # get_iotdb_data.delete_data(new_iotdb, session_pool, insert_data_list, 1761138000000)
# get_iotdb_data.insert_np_tablet(
#     new_iotdb, session_pool, device_id, measurements, data_types,
#     np_values, np_timestamps
# )

# get_iotdb_data.test_connection(new_iotdb, session_pool)

# start_time = int(time.mktime(time.strptime(query_times["start_time"], "%Y-%m-%d %H:%M:%S")))
# end_time = int(time.mktime(time.strptime(query_times["end_time"], "%Y-%m-%d %H:%M:%S")))
# result = get_iotdb_data.get_data(new_iotdb, session_pool, query_data_list, start_time, end_time, query_times["interval"])
# print(result)
query = "SELECT first_value(temp) AS temp, first_value(press) AS press FROM root.test_group.tq_tank_1 GROUP BY ([2025-10-22T12:00:00.000, 2025-10-22T18:00:00.000),30m)"

results = get_iotdb_data.execute_query(new_iotdb, session_pool, query)
# while results.has_next():
#     row = results.next()
#     print(row)
df_results = results.todf()
df_results["Time"] = (pd.to_datetime(df_results["Time"], unit='ms', utc=True)
                      .dt.tz_convert("Asia/Shanghai")
                      .dt.tz_localize(None)  # 去掉时区信息
                      )
print(df_results)




atexit.register(new_iotdb.close_session_pool, session_pool)
