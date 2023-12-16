import sys
import logging
import asyncio

import bot.bot as start_bot


async def main():
    # db.start_session()
    await start_bot.main()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f'Exit! - {exception}')
