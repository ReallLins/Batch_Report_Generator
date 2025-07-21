from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
from contextlib import contextmanager

# @st.cache_resource(show_spinner=False)
class DatabaseConfig:
    def __init__(self, host: str, port: str, name: str, username: str, password: str):
        self.host = host
        self.port = port
        self.name = name
        self.username = username
        self.password = password


    def get_engine(self):
        # if not all([self.host, self.port, self.name, self.username, self.password]):
        #     st.error("数据库配置信息不完整，请检查 secrets.toml 文件")
        #     st.stop()
        db_url = f"mssql+pymssql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"
        engine = create_engine(
            db_url, 
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            # fast_executemany=True,
        )
        return engine

    @contextmanager
    def get_session(self):
        engine = self.get_engine()
        session = sessionmaker(bind=engine)()
        try:
            yield session
        except ValueError as e:
            session.rollback()
            print(f"操作失败: {e}")
            # st.error(f"数据库操作失败: {e}")
        finally:
            session.close()
