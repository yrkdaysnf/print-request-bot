import sqlite3 as sq

async def db_start():
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()

    # Создание таблицы для пользователей
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY, 
                balance INTEGER DEFAULT 0
                )
                ''')
    # Создание таблицы для файлов
    cur.execute(
                '''CREATE TABLE IF NOT EXISTS files(
                file_id INTEGER PRIMARY KEY, 
                user_id INTEGER, 
                date_sent TEXT,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                ''')
    db.commit()
    db.close()

async def create_user(user_id):
    db = sq.connect('core\\data\\database.sql')
    cur = db.cursor()

    user = cur.execute("SELECT 1 FROM users WHERE user_id == ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?,?)",(user_id, 0))
        db.commit()
    db.close()
