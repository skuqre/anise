import disnake, os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Anise(commands.InteractionBot):
    async def on_ready(self):
        await self.change_presence(status=disnake.Status.idle)
        
        print(f"Locked and loaded. Logged on as {self.user}\n------")


def main():
    bot = Anise()
    bot.load_extensions(os.path.join(__package__, 'cogs'))
    bot.run(os.environ.get("bot_secret"))