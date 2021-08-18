import asyncio
import json
import time
from datetime import datetime, timedelta

import schedule

from bot import *


def startTread(bot, settings):
    asyncio.run(check(bot, settings))


async def check(bot, settings):
    t1, t2 = settings
    data = loadData()
    if data:
        t, checked, msg_id = data
        time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        if not checked:
            if time + timedelta(hours=t2) < datetime.now():
                await bot.summarize()
                saveData(True, msg_id)
                return
            else:
                return
        else:
            if time + timedelta(hours=t1) >= datetime.now():
                return
    msg_id = await bot.send_message()
    saveData(False, msg_id)


def saveData(check, msg_id):
    time = datetime.now()
    with open(CACHE_FILE, "w") as json_file:
        json.dump({"time": str(time), "checked": check, "msg_id": msg_id}, json_file)


def loadData():
    try:
        f = open(CACHE_FILE)
        data = json.load(f)
        time = data["time"]
        checked = data["checked"]
        msg_id = data["msg_id"]
        f.close()
        return time, checked, msg_id
    except Exception as e:
        return None


def loadSettings():
    try:
        f = open(SETTING_FILE)
        data = json.load(f)
        return data["time_between_messages"], data["time_to_react"]
    except Exception as e:
        return None


def main():
    data = loadData()
    if data:
        _, _, msg_id = data
    else:
        msg_id = None

    settings = loadSettings()
    bot = Bot(msg_id)

    # schedule.every(10).minutes.do(startTread, bot=bot)
    schedule.every(2).seconds.do(startTread, bot=bot, settings=settings)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
