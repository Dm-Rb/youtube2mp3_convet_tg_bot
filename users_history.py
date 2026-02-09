import aiosqlite
import sqlite3


class UsersHistory:
    database_file = 'history.db'

    def __init__(self):
        self.__create_table()

    def __create_table(self):
        with sqlite3.connect(self.database_file) as conn:
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS users_history (
                    tg_user_id INTEGER NOT NULL,
                    tg_user_full_name TEXT,
                    file_title TEXT,
                    tg_file_id TEXT,
                    mp3_bitrate INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )'''
            )
            conn.commit()

    async def add_new_row(self, tg_user_id, tg_user_full_name, file_title, tg_file_id, mp3_bitrate):
        async with aiosqlite.connect(self.database_file) as conn:

            await conn.execute(
                """INSERT INTO users_history 
                (tg_user_id, tg_user_full_name, file_title, tg_file_id, mp3_bitrate) 
                VALUES (?, ?, ?, ?, ?)""",
                (tg_user_id, tg_user_full_name, file_title, tg_file_id, mp3_bitrate)
            )
            await conn.commit()

    async def get_user_history(self, tg_user_id):
        async with aiosqlite.connect(self.database_file) as conn:
            cursor = await conn.execute(
                "SELECT * FROM users_history WHERE tg_user_id = ? ORDER BY timestamp DESC",
                (tg_user_id,)
            )
            rows = await cursor.fetchall()
            return rows


data_base_obj = UsersHistory()
