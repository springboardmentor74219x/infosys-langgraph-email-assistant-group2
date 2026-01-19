import os
from sqlalchemy import create_engine, Table, Column, String, MetaData

# Resolve project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "memory.db")
print("Using memory DB at:", DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}")
metadata = MetaData()

memory_table = Table(
    "memory",
    metadata,
    Column("user", String),
    Column("key", String),
    Column("value", String),
)

metadata.create_all(engine)


def save_memory(user, key, value):
    with engine.connect() as conn:
        conn.execute(
            memory_table.insert().values(user=user, key=key, value=value)
        )


def get_memory(user):
    with engine.connect() as conn:
        rows = conn.execute(
            memory_table.select().where(memory_table.c.user == user)
        )
        return {r.key: r.value for r in rows}