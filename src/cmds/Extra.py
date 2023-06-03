import discord
import util
from discord import app_commands as acd
from discord.ext import commands

# Extra/other stuff.

class extra(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @acd.command(name='ping', description='Pong! 🏓')
    async def ping(self, itcn: discord.Interaction):
        data = f"**Latency**: {round(self.bot.latency * 1000, 1)}ms"
        embed = util.quick_embed('Pong! 🏓', data.strip())
        await itcn.response.send_message(embed=embed)
