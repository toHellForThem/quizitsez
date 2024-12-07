from core import DB_NAME, aiosqlite
from reload import get_question


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, user_name CHAR, question_index INTEGER, user_score INTEGER)"""
        )
        await db.commit()


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    user_name = message.from_user.username
    await update_quiz_index(user_id, user_name, current_question_index)
    await get_question(message, user_id)


async def update_quiz_index(user_id, user_name, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO quiz_state (user_id, user_name, question_index) VALUES (?, ?, ?)",
            (user_id, user_name, index),
        )
        await db.commit()


async def get_user_score(id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_score FROM quiz_state WHERE user_id = (?)",
            (id,),
        ) as cursor:
            results = await cursor.fetchone()
            print(results)
            if results[0] is None:
                return 0

            return results[0]


async def update_user_score(id, user_score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            f"UPDATE quiz_state SET user_score = {user_score} WHERE user_id = {id}",
        )
        await db.commit()


async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_name, user_score FROM quiz_state ORDER BY user_score",
        ) as cursor:
            results = await cursor.fetchall()
            if results is not None:
                return results
            else:
                return 0
