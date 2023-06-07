import disnake
import src.util as util
from disnake.ext import commands as cmds


class AdminCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot

def setup(bot: cmds.Bot) -> None:
    bot.add_cog(AdminCommands(bot))
    print("Admin commands loaded!")