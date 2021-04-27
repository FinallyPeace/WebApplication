import sqlite3
connect = sqlite3.connect('database.db')
print("Opened database successfully")

connect.execute(
    """
    CREATE TABLE students (
        name TEXT,
        city TEXT,
        pin TEXT,
        addr TEXT
    )
    """
)
print("Table created successfully")
connect.close()