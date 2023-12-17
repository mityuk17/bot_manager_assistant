import sys
import logging
import asyncio

import bot.bot as start_bot
# from db.db import create_tables


async def main():
    # await create_tables()
    await start_bot.main()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f'Exit! - {exception}')
