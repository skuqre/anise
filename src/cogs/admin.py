import disnake
import src.util as util
from disnake.ext import commands as cmds


class AdminCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot

    @cmds.has_permissions(manage_messages=True)
    @cmds.slash_command(name='purge', description="Erase messages.")
    async def purge(self, itcn: disnake.CommandInteraction, amount: int):
        await itcn.response.defer(with_message=False, ephemeral=True)
        await itcn.send(embed=util.quick_embed("Purging!", f"Deleting {amount} messages..."), ephemeral=True)
        await itcn.channel.purge(limit=amount)
        await itcn.send(embed=util.quick_embed("Purged!", f"Deleted {amount} messages."), ephemeral=True)
        


def setup(bot: cmds.Bot) -> None:
    bot.add_cog(AdminCommands(bot))
    print("Admin commands loaded!")