import asyncio
from connect import create_table
from core import dp, bot
from listeners import setListeners


async def main():
    await create_table()
    setListeners(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
