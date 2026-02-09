from sqlalchemy import create_engine, Table, Column, String, MetaData

engine = create_engine("sqlite:///data/memory.db")
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
        conn.execute(memory_table.insert().values(user=user, key=key, value=value))

def get_memory(user):
    with engine.connect() as conn:
        rows = conn.execute(memory_table.select().where(memory_table.c.user == user))
        return {r.key: r.value for r in rows}