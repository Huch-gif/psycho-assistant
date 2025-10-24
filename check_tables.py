# check_tables.py
import sqlite3

conn = sqlite3.connect('psycho.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в БД:", [t[0] for t in tables])
conn.close()