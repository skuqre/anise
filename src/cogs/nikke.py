import disnake
from disnake.ext import commands as cmds

class NikkeCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot

    @cmds.slash_command(name='nikke')
    async def nikke(self, itcn: disnake.CommandInteraction):
        pass

    @nikke.sub_command(name='what', description='What is NIKKE?')
    async def what(self, itcn: disnake.CommandInteraction):
        pass

    @nikke.sub_command(name='info', description='Display NIKKE character info.')
    async def info(self, itcn: disnake.CommandInteraction):
        pass

    @nikke.sub_command(name='skills', description='Display NIKKE character skill info.')
    async def skills(self, itcn: disnake.CommandInteraction):
        pass

    @nikke.sub_command(name='image', description='Display NIKKE character images. 3 types included.')
    async def image(self, itcn: disnake.CommandInteraction):
        pass

def setup(bot: cmds.Bot) -> None:
    bot.add_cog(NikkeCommands(bot))