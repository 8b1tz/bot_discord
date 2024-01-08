import os

POSTGRES_DB = os.environ.get("POSTGRES_DB", "app")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa