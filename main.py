import asyncio
import time

from bot import Bot


async def main():
    b = Bot()

    await b.debug()
    await b.send_message()
    time.sleep(10)
    await b.summarize()


asyncio.run(main())
