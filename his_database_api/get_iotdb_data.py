from iotdb_config import IotdbConfig
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.utils.NumpyTablet import NumpyTablet
import atexit
import numpy as np

def test_connection(iotdb_config: IotdbConfig, session_pool):
    with iotdb_config.get_session(session_pool) as session:
        print(f"Connection to IoTDB successful.")

def create_storage_group(iotdb_config: IotdbConfig, session_pool, group_name: str):
    with iotdb_config.get_session(session_pool) as session:
        session.set_storage_group(group_name)
        print(f"Storage group '{group_name}' created successfully.")

def delete_storage_group(iotdb_config: IotdbConfig, session_pool, group_name: str):
    with iotdb_config.get_session(session_pool) as session:
        session.delete_storage_group(group_name)
        print(f"Storage group '{group_name}' deleted successfully.")

def insert_np_tablet(iotdb_config: IotdbConfig, session_pool, device_id: str,
                     measurements: list, data_types: list,
                     np_values: list, np_timestamps: np.ndarray):
    np_tablet = NumpyTablet(
        device_id, measurements, data_types, np_values, np_timestamps
        )
    with iotdb_config.get_session(session_pool) as session:
        session.insert_tablet(np_tablet)
        print(f"Data inserted into device '{device_id}' successfully.")

def delete_data(iotdb_config: IotdbConfig, session_pool, paths: list, endtime: int):
    with iotdb_config.get_session(session_pool) as session:
        session.delete_data(paths, endtime)
        print(f"Data at paths {paths} deleted successfully.")

def get_data_point_value(iotdb_config: IotdbConfig, session_pool, paths: list, start_time: int, end_time: int, interval: int):
    with iotdb_config.get_session(session_pool) as session:
        sql = f"SELECT {', '.join(paths)} FROM root.test_group GROUP BY ([{start_time}, {end_time}), {interval}s)"
        result = session.execute_query_statement(sql)
        session.execute_aggregation_query(sql)
        df_result = result.todf()
        return df_result

def execute_query(iotdb_config: IotdbConfig, session_pool, sql: str):
    with iotdb_config.get_session(session_pool) as session:
        result = session.execute_query_statement(sql)
        return result

