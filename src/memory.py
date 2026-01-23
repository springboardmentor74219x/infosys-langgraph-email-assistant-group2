from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite-based persistent memory
memory = SqliteSaver.from_conn_string("memory.db")
