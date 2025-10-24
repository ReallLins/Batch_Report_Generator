from iotdb.Session import Session
from iotdb.SessionPool import PoolConfig, SessionPool
from contextlib import contextmanager

def get_iotdb_config():
    return IotdbConfig()

class IotdbConfig:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "6667"
        self.username = "root"
        self.password = "root"
    
    def create_session_pool(self):
        pool_config = PoolConfig(host=self.ip, port=self.port, user_name=self.username,password=self.password,
                                 fetch_size=1024,time_zone="UTC+8", max_retry=3)
        max_pool_size = 5
        wait_timeout_ms = 3000
        session_pool = SessionPool(pool_config, max_pool_size, wait_timeout_ms)
        return session_pool

    @contextmanager
    def get_session(self, session_pool: SessionPool):
        session = session_pool.get_session()
        try:
            yield session
        except Exception as e:
            print(f"IotDB操作失败: {e}")
        finally:
            session_pool.put_back(session)
    
    def close_session_pool(self, session_pool: SessionPool):
        session_pool.close()