import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Redes/basecpf.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# For each table, get its columns
for table_name in tables:
    table = table_name[0]
    print(f"Table: {table}")

    cursor.execute(f"PRAGMA table_info('{table}');")
    columns = cursor.fetchall()

    for column in columns:
        print(f"  - {column[1]} ({column[2]})")  # column[1] = name, column[2] = type

conn.close()
