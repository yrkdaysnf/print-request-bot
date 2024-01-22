import sqlite3 as sq

async def db_start():
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()

    # Создание таблицы для пользователей
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY, 
                username TEXT,
                balance REAL DEFAULT 0
                )
                ''')
    # Создание таблицы для файлов
    cur.execute(
                '''CREATE TABLE IF NOT EXISTS files(
                file_id INTEGER PRIMARY KEY, 
                user_id INTEGER, 
                date_sent TEXT,
                status TEXT,
                price INTEGER,
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
    try:
        cur.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,))
        balance = cur.fetchone()
        return balance[0]
    finally:
        db.close()

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
        cur.execute("SELECT user_id, username, balance FROM users")
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