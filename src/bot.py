import disnake, os
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake.interactions import ApplicationCommandInteraction
from dotenv import load_dotenv

load_dotenv()

IS_DEBUG = os.getenv("is_debug", 'False') == 'True'


class Anise(commands.InteractionBot):
    async def on_ready(self):
        print(f"Hello chat. Logged on as {self.user}\n------")


def main():
    bot = Anise(reload=IS_DEBUG, status=disnake.Status.idle)

    bot.load_extensions(os.path.join(__package__, 'cogs'))
    bot.run(os.getenv("bot_secret"))
    bot.clear()