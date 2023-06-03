import os
import discord
from discord.ext import commands
from cmds.NIKKE import nikke
from cmds.Extra import extra
from dotenv import load_dotenv

load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='a!', intents=intents)
bot.tree.add_command(nikke(bot))

@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    print("------------")

    await bot.add_cog(extra(bot))

    # await bot.tree.sync()

bot.run(os.environ.get("bot_secret"))