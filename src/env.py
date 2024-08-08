import os

from dataclasses import dataclass


@dataclass
class PostgresEnv:
    host: str = os.environ.get("POSTGRES_HOST", "localhost")
    port: str = os.environ.get("POSTGRES_PORT", "5432")
    user: str = os.environ.get("POSTGRES_USER", "postgres")
    password: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    db: str = os.environ.get("POSTGRES_DB", "postgres")

    @classmethod
    def get_conn_string(cls):
        return f"postgresql://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.db}"


@dataclass
class SourceEnv:
    name: str = os.environ.get("SOURCE_NAME", "wiki")
