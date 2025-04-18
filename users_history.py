import aiosqlite
import sqlite3


class UsersHistory:

    database_file = 'history.db'

    def __init__(self):
        self.__create_table()

        # типа хеш с pos
    def __create_table(self):
        with sqlite3.connect(self.database_file) as conn:
            conn.execute(
                f'''
                CREATE TABLE IF NOT EXISTS users_history (
                    tg_user_id INTEGER NOT NULL,
                    file_title TEXT UNIQUE NOT NULL,
                    tg_file_id NTEGER NOT NULL
                )
                '''
            )
            conn.commit()

    async def add_new_row(self, tg_user_id, file_title, tg_file_id):
        async with aiosqlite.connect(self.database_file) as conn:

            await conn.execute(
                "INSERT INTO users_history (tg_user_id, file_title, tg_file_id) VALUES (?, ?, ?)",
                (tg_user_id, file_title, tg_file_id,)
            )
            await conn.commit()
            await conn.close()
        return


data_base_obj = UsersHistory()
