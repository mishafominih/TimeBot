import asyncio

import Bot

bot = Bot.TelBot("2055521852:AAGZjBA1A8b52Umua11fPlSGhPLJQk0oIYA")

loop = asyncio.get_event_loop()

loop.create_task(bot.start())
loop.run_forever()
