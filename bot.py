import json
import random

import fbchat

SETTING_FILE = "settings.json"


class Bot:
    def __init__(self):
        self.session = None
        self.client = None
        self.thread = None
        self.msg_id = None
        self.settings = json.load(open(SETTING_FILE, encoding="utf-8"))

    async def _init(self):

        self.session = await fbchat.Session.login(
            self.settings["email"], self.settings["password"]
        )
        self.client = fbchat.Client(session=self.session)
        self.thread = await self._transform_data(
            self.client.fetch_thread_info(self.settings["group_id"])
        )

        if type(self.thread) != fbchat.GroupData:
            print(f"Thread {self.settings['group_id']} is not group!")
            exit()

    async def _transform_data(self, data):
        async for t in data:
            return t

    async def _send_message(self):
        self.msg_id, _ = await self.thread.send_text(
            random.choice(self.settings["message"])
        )

    async def _get_reactions(self):
        async for msg in self.thread.fetch_messages(limit=100):
            if msg.id == self.msg_id:
                return list(msg.reactions)

    async def _summarize(self):
        users_ids = await self._get_reactions()
        if len(users_ids) < 2:
            await self.thread.send_text(random.choice(self.settings["error"]))
        else:
            random.shuffle(users_ids)
            users_in_thread = await self.client.fetch_users()
            for user_id in users_ids:
                user_name = "Coś poszło nie tak"
                for user in users_in_thread:
                    if user_id == user.id:
                        user_name = user.name
                        break
                await self.thread.send_text(
                    text="@" + user_name,
                    mentions=[
                        fbchat.Mention(
                            thread_id=user_id, offset=0, length=len(user_name) + 1
                        )
                    ],
                )

    async def _logout(self):
        await self.session.logout()

    async def send_message(self):
        await self._init()
        await self._send_message()
        await self._logout()

    async def summarize(self):
        await self._init()
        await self._summarize()
        await self._logout()

    async def debug(self):
        await self._init()
        print("===============================")
        print(f"Bot user id: {self.session.user.id}")
        print("Available chats:")
        async for t in self.client.fetch_threads(limit=100):
            print(t.name, "-", t.id)
        print("===============================")
        print("")
        await self._logout()
