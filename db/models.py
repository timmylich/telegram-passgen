import aiosqlite
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.db')

class Database:
    _instance = None

    def __new__(cls, db_path: str = None):
        if not cls._instance:
            if db_path is None:
                raise ValueError("DB not connected.")
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._db_path = db_path
            cls._instance._connection = None
        return cls._instance

    async def connect(self):
        if not self._connection:
            self._connection = await aiosqlite.connect(self._db_path)
            await self._connection.execute("PRAGMA foreign_keys = ON;")
            await self._connection.commit()

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
    
    async def insertUser(self, tg_id):
        await self.connect()
        async with self._connection.execute(f"INSERT INTO users (tg_id, regdate) VALUES ({tg_id}, {int(time.time())})") as cursor:
            await self._connection.commit()
            return cursor
        
    async def setUserLang(self, tg_id, lang):
        await self.connect()
        async with self._connection.execute(f"UPDATE users SET lang = '{lang}' WHERE tg_id = {tg_id}") as cursor:
            await self._connection.commit()
            return cursor
        
    async def getUserLang(self, tg_id):
        await self.connect()
        self._connection.row_factory = aiosqlite.Row
        async with self._connection.execute(f"SELECT lang FROM users WHERE tg_id = {tg_id} LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if(row == None): return 'ru'
            return row['lang']
    
    async def isUserInDB(self, tg_id):
        await self.connect()
        async with self._connection.execute(f"SELECT COUNT (*) AS count FROM users WHERE tg_id = {tg_id} LIMIT 1") as cursor:
            row = await cursor.fetchone()
            return row is not None
        
db = Database(DB_PATH)