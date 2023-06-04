import os
import discord, asyncio
from discord.ext import commands, tasks
from cmds.NIKKE import nikke
from cmds.Extra import extra
from cmds.Admin import role
from dotenv import load_dotenv

load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='a!', intents=intents)
bot.tree.add_command(nikke(bot))
bot.tree.add_command(role(bot))

@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    print("------------")

    loop.start()

    await bot.add_cog(extra(bot))
    await bot.tree.sync()

@tasks.loop(seconds=10)
async def loop():
    await bot.change_presence(status=discord.Status.idle)

bot.run(os.environ.get("bot_secret"))