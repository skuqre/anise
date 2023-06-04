import asyncio
import discord
import util
from discord import app_commands as acd
from discord.ext import commands

whereis = {}
places = [
    {"place": "Command Center", "img": "command_center", "doings": [
        "Getting yet another soda from the fridge.",
        "Using the Commander's shower...",
        "Recollecting memories.",
        "Getting advise from the Commander."
    ]},
    {"place": "Ark", "img": "ark", "doings": [
        "Going to the Royal Road.",
        "Walking around."
    ]},
    {"place": "Royal Road", "img": "royal_road", "doings": [
        "Shopping.",
        "Shopping... again.",
        "Looking around what to buy next.",
    ]},
    {"place": "Outer Rim", "img": "outer_rim", "doings": [
        "Leaving",
        "Getting the hell outta there",
        "Departing",
        "Leaving",
        "Leaving",
        "Leaving",
        "Leaving"
    ]},
    {"place": "Ark", "img": "fast_food", "doings": [
        "Gettin' food.",
        "Getting splendamin nutrients.",
    ]},
]

shitshesays = [
    "Wanna know a thing? The commander has been rumored to have had the _dirty doo_ with multiple Nikkes. I don't know if that's true or not, don't quote me on that.",
    
]

# Extra/other stuff.

class extra(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @acd.command(name='ping', description='🏓 Pong! Returns bot latency in milliseconds.')
    async def ping(self, itcn: discord.Interaction):
        data = f"**Latency**: {round(self.bot.latency * 1000, 1)}ms"
        embed = util.quick_embed('Pong! 🏓', data.strip())
        await itcn.response.send_message(embed=embed)

    @acd.command(name='whereisanisé', description='Where is she? Results vary and depend on the hour of the day.')
    async def whereis(self, itcn: discord.Interaction):
        embed = util.quick_embed('Where is she?', '')
        embed.description = f"She's currently at the **{123}**.\nWhat's she doing? **{321}**"
        await itcn.response.send_message(embed=embed)
