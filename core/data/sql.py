import sqlite3 as sq
from datetime import datetime

async def db_start():
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()

    # Создание таблицы для пользователей
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER, 
                username TEXT,
                balance REAL DEFAULT 0,
                PRIMARY KEY("user_id")
                )
                ''')
    # Создание таблицы для файлов
    cur.execute(
                '''CREATE TABLE IF NOT EXISTS files(
                unique_id TEXT,
                file_id TEXT,
                user_id INTEGER,
                date_sent TEXT,
                price INTEGER,
                status TEXT DEFAULT queue,
                file_name TEXT,
                PRIMARY KEY("unique_id"),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                ''')
    db.commit()
    db.close()

async def create_user(user_id:int, username:str):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    user = cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if user:
        if user[0] != username:
            cur.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            db.commit()
    else:
        cur.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        db.commit()
    db.close()

async def get_balance(user_id:int):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,))
    balance = cur.fetchone()
    db.close()
    return balance[0]

async def get_username(user_id:int):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE user_id = ?",(user_id,))
        username = cur.fetchone()
        return username[0]
    finally:
        db.close()

async def get_all_users():
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        return result
    finally:
        db.close()

async def edit_user_balance(user_id: int, new_balance: float):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    cur.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
    db.commit()
    db.close()

async def create_file(unique_id: str, file_id: str, user_id: int, price: float, file_name:str):
    date_sent = datetime.now().strftime('%d.%m.%Y - %H:%M')
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    cur.execute("INSERT INTO files (unique_id, file_id ,user_id, date_sent, price, file_name) VALUES (?, ?, ?, ?, ?, ?)", (unique_id, file_id ,user_id, date_sent, price, file_name))
    db.commit()
    db.close()

async def edit_file_status(unique_id: str, new_status: str):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    cur.execute("UPDATE files SET status=? WHERE unique_id=?", (new_status, unique_id))
    db.commit()
    db.close()

async def get_fileinfo(unique_id:str):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    try:
        cur.execute("SELECT file_id, user_id, date_sent, price, status FROM files WHERE unique_id=?", (unique_id,))
        fileinfo = cur.fetchone()
        return fileinfo
    finally:
        db.close()

async def get_all_files_in_status(status):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    try:
        cur.execute("SELECT unique_id, user_id, date_sent, file_name FROM files WHERE status = ?",(status,))
        result = cur.fetchall()
        return result
    finally:
        db.close()

async def get_all_myfiles(user_id):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()
    try:
        cur.execute("SELECT unique_id, date_sent, status, file_name FROM files WHERE user_id = ?",(user_id,))
        result = cur.fetchall()
        return result
    finally:
        db.close()
