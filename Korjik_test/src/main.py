import asyncio
import logging
import sys

from config.environment import BOT_TOKEN
from core.application import Application


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    while True:
        app = Application(BOT_TOKEN)
        await app.initialize()
        if not await app.run():
            break


if __name__ == "__main__":
    asyncio.run(main())
