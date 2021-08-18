import asyncio
import time

from PyInquirer import prompt

from bot import Bot


async def main():
    b = Bot()
    while True:
        v = prompt(
            {
                "type": "list",
                "name": "a",
                "message": "What you want to do?",
                "choices": [
                    {"name": "Debug", "value": 1},
                    {"name": "Send Message", "value": 2},
                    {"name": "Summarize", "value": 3},
                    {"name": "Exit", "value": 4},
                ],
            }
        )["a"]

        if v == 1:
            await b.debug()
        elif v == 2:
            await b.send_message()
        elif v == 3:
            await b.summarize()
        else:
            exit()


asyncio.run(main())
