import disnake
import os
from random import Random as Rnd
from disnake.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

IS_DEBUG = os.getenv("is_debug", 'False') == 'True'


class Anise(commands.InteractionBot):
    async def on_ready(self):
        print(f"\nLet's get this party started!\nLogged in as {self.user}\n")

        await self.random_status_loop.start()

    @tasks.loop(minutes=15.0)
    async def random_status_loop(self):
        statuses = open("data/status.txt", "r").read().strip().splitlines()
        await self.change_presence(activity=disnake.CustomActivity(name=Rnd().choice(statuses)), status=disnake.Status.idle)


def main():
    intents = disnake.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = Anise(reload=IS_DEBUG, status=disnake.Status.idle, intents=intents)

    bot.load_extensions(os.path.join(__package__, 'cogs'))
    bot.run(os.getenv("bot_secret"))
    bot.clear()
