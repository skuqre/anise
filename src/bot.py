import disnake, os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Anise(commands.InteractionBot):
    async def on_ready(self):
        print(f"Locked and loaded. Logged on as {self.user}\n------")

bot = Anise()

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message(f"Pong! {round(bot.latency * 1000, 1)}ms.")

bot.run(os.environ.get("bot_secret"))