from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

def get_database_config():
    return DatabaseConfig()

def get_engine(database_config) -> Engine:
    return database_config.get_engine()

class DatabaseConfig:
    def __init__(self):
        self.host = "localhost"
        self.port = "5432"
        self.name = "postgres"
        self.username = "root"
        self.password = "Admin_1"

    def get_engine(self) -> Engine:
        if not all([self.host, self.port, self.name, self.username, self.password]):
            raise ValueError("数据库连接信息不完整，请检查配置。")
        db_url = f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"
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
    def get_session(self, engine: Engine):
        session = sessionmaker(bind=engine)()
        try:
            yield session
        except ValueError as e:
            session.rollback()
            raise ValueError(f"操作失败: {e}")
        finally:
            session.close()
