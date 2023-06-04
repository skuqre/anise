import discord, asyncio
from discord import app_commands as acd
from discord.ext import commands
import util


class role(acd.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @acd.command(name='add', description='Create a simple role.')
    @acd.checks.has_permissions(manage_roles=True)
    @acd.checks.bot_has_permissions(manage_roles=True)
    @acd.choices(permissions_group=[
        acd.Choice(name="Admin", value="0"), 
        acd.Choice(name="Member", value="1"), 
        acd.Choice(name="Goner", value="2")
    ])
    async def add(self, itcn: discord.Interaction, role_name:str, hex_color:str, permissions_group:acd.Choice[str], to_member:discord.Member = None, separate:bool = False, mentionable:bool = False):
        grp: discord.Permissions = None

        match permissions_group.value:
            case "0":
                grp = discord.Permissions.elevated()
            case "1":
                grp = discord.Permissions.membership()
            case "2":
                grp = discord.Permissions.none()

        try:
            role: discord.Role = await itcn.guild.create_role(name=role_name, colour=int(hex_color, 16), permissions=grp, hoist=separate, mentionable=mentionable)
            await itcn.response.send_message(embed=util.quick_embed("Done!", f"Role <@&{role.id}> created successfully.", 0x55fe6d), ephemeral=True)
            if to_member:
                await to_member.add_roles(role)
                await itcn.followup.send(embed=util.quick_embed("", f"User <@{to_member.id}> has been added the role as well.", 0x55fe6d), ephemeral=True)
        except:
            embed = util.quick_embed('Forbidden!', 'You are not able to use this command!', 0xff3d33)
            await itcn.response.send_message(embed=embed, ephemeral=True)

    @acd.command(name='del', description='Delete a role.')
    @acd.checks.has_permissions(manage_roles=True)
    @acd.checks.bot_has_permissions(manage_roles=True)
    async def _del(self, itcn: discord.Interaction, role: discord.Role, reason: str = ''):
        try:
            immut = role.name
            await role.delete(reason=reason)
            await itcn.response.send_message(embed=util.quick_embed("Deleted!", f"Role {immut} has been deleted.", 0x55fe6d), ephemeral=True)
        except:
            embed = util.quick_embed('Forbidden!', 'You are not able to use this command!', 0xff3d33)
            await itcn.response.send_message(embed=embed, ephemeral=True)