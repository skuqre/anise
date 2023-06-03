import json
import discord, asyncio
from discord import app_commands as acd
from discord.ext import commands
import requests
import util

# Request NIKKE data. Low and behold my awesome error-handling skills
def request_nikke(character:str):
    try:
        data = requests.get(f'https://www.prydwen.gg/page-data/nikke/characters/{util.kebab(character)}/page-data.json')
        data = data.json()
        return data
    except:
        return None
    
def format_skilldesc(desc:str):
    tor = desc.strip()
    if ":" in desc:
        tor = "**" + tor.replace(":", "**:")
    elif desc.startswith('■'):
        return tor
    else:
        tor = "**" + tor + "**"
    return tor

# Stores most commands that relates to Goddess of Victory: NIKKE.
# Data comes from https://www.prydwen.gg. Go visit!
class nikke(acd.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @acd.command(name='info', description='Provide basic NIKKE character information.')
    async def info(self, itcn: discord.Interaction, character:str):
        data = request_nikke(character)
        await itcn.response.defer(ephemeral=True, thinking=True)

        if data is None:
            embed = util.quick_embed('Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await itcn.followup.send(embed=embed)
            await asyncio.sleep(4)
            return

        nikke = data['result']['data']['currentUnit']['nodes'][0]

        embed = discord.Embed()
        embed.set_author(name="Character Info")
        embed.title = nikke['name']

        # Why can you be null? Shouldn't every NIKKE have some lore by now?
        if not nikke['backstory'] is None:
            embed.description = nikke['backstory']['backstory'] + '\n'

        embed.set_thumbnail(url='https://www.prydwen.gg' + nikke['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        # Personal
        personal = f"""
        **Full name**: {nikke['name']}
        **Manufacturer**: {nikke['manufacturer']}
        **Squad**: {nikke['squad']}
        **Weapon**: {nikke['weaponName']}
        """
        embed.add_field(name="Personal", value=personal.strip(), inline=True)

        # Combat
        combat = f"""
        **Rarity**: {nikke['rarity']}
        **Class**: {nikke['class']}
        **Weapon**: {nikke['weapon']}
        **Element**: {nikke['element']}
        **Burst Type**: `{int(nikke['burstType']) * 'I'}`
        """
        embed.add_field(name="Combat", value=combat.strip(), inline=True)

        embed.set_footer(text="Data from https://www.prydwen.gg! Go visit!")

        match nikke['rarity']:
            case 'R':
                embed.color = 0x0090ff
            case 'SR':
                embed.color = 0xbf00fe
            case 'SSR':
                embed.color = 0xffc000

        misc = f"""
        **Release date**: {nikke['releaseDate']}
        **VA (:flag_kr:)**: {nikke['cv']['kr']}
        **VA (:flag_jp:)**: {nikke['cv']['jpn']}
        **VA (:flag_us:)**: {nikke['cv']['en']}
        """
        embed.add_field(name="Miscellaneous", value=misc.strip(), inline=False)

        if not nikke['specialities'] is None:
            embed.add_field(name="Specialities", value='\n'.join(nikke['specialities']), inline=True)
            
        await asyncio.sleep(4)
        await itcn.followup.send(embed=embed)

    @acd.command(name='image', description='Provides NIKKE images. Full body, card bust, head bust.')
    @acd.describe(type="Image type.")
    @acd.choices(type=[acd.Choice(name="Full Body", value="0"), acd.Choice(name="Card Bust", value="1"), acd.Choice(name="Head Bust", value="2")])
    async def image(self, itcn: discord.Interaction, character:str, type:acd.Choice[str]):
        data = request_nikke(character)
        await itcn.response.defer(ephemeral=True, thinking=True)

        if data is None:
            embed = util.quick_embed('Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await asyncio.sleep(4)
            await itcn.followup.send(embed=embed)
            return

        nikke = data['result']['data']['currentUnit']['nodes'][0]

        embed = util.quick_embed('', '')
        embed.title = nikke['name']

        imageType = 'smallImage'

        match type.value:
            case "0":
                imageType = 'fullImage'
                embed.set_author(name="Full Body Image")
            case "1":
                imageType = 'cardImage'
                embed.set_author(name="Card Bust Image")
            case "2":
                imageType = 'smallImage'
                embed.set_author(name="Head Bust Image")


        embed.set_image(url='https://www.prydwen.gg' + nikke[imageType]['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        await asyncio.sleep(4)
        await itcn.followup.send(embed=embed)

    # Probably the longest command yet
    @acd.command(name='skills', description='Provide NIKKE character skill information.')
    async def skills(self, itcn: discord.Interaction, character:str, max_level:bool=False):
        data = request_nikke(character)
        await itcn.response.defer(ephemeral=True, thinking=True)

        if data is None:
            embed = util.quick_embed('Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await asyncio.sleep(4)
            await itcn.followup.send(embed=embed)
            return

        nikke = data['result']['data']['currentUnit']['nodes'][0]
        
        skill1_name = nikke['skills'][0]['name']
        skill2_name = nikke['skills'][1]['name']
        burst_name = nikke['skills'][2]['name']
        sight = "sight_"
        level = "descriptionLevel10" if max_level else "descriptionLevel1"

        match nikke['weapon']:
            case 'Assault Rifle':
                sight += 'assault'
            case 'Minigun':
                sight += 'minigun'
            case 'Rocket Launcher':
                sight += 'rocket'
            case 'Shotgun':
                sight += 'shotgun'
            case 'SMG':
                sight += 'smg'
            case 'Sniper Rifle':
                sight += 'sniper'

        embed = util.quick_embed('', '')
        embed.title = nikke['name'] + '\'s Skills'
        embed.description = f"""
        Her skills include **{skill1_name}** and **{skill2_name}**, and her burst being **{burst_name}**.
        Information listed below is in **{"Level 10" if max_level else "Level 1"}**.
        """.strip()
        embed.set_thumbnail(url='https://www.prydwen.gg' + nikke['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        # NORMAL ATTACK

        normal_data = json.loads(nikke['basicAttack']['raw'])
        normal_embed = util.quick_embed('Normal Attack', '')
        for item in normal_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']
                
            normal_embed.description += format_skilldesc(complete) + "\n"

        normal_embed.add_field(name="Control Type", value=f"{nikke['controlMode']}", inline=True)
        normal_embed.add_field(name="Capacity", value=f"{nikke['ammoCapacity']} ammo", inline=True)
        normal_embed.add_field(name="Reload Time", value=f"{nikke['reloadTime']} seconds", inline=True)

        sight_upload = discord.File(f'img\sights\{sight}.png', filename='sight.png')
        normal_embed.set_thumbnail(url='attachment://sight.png')

        # SKILL 1

        skill1_data = json.loads(nikke['skills'][0][level]['raw'])
        skill1_embed = util.quick_embed(f'Skill 1 - {skill1_name}', '')
        for item in skill1_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']
                
            skill1_embed.description += format_skilldesc(complete) + "\n"

        skill1_upload = discord.File(f'img\icon_skill1.png', filename='skill1.png')
        skill1_embed.set_thumbnail(url='attachment://skill1.png')

        skill1_embed.add_field(name="Type", value=f"{nikke['skills'][0]['type']}", inline=True)
        skill1_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][0]['cooldown'] is None else str(nikke['skills'][0]['cooldown']) + ' seconds'}", inline=True)

        # SKILL 2

        skill2_data = json.loads(nikke['skills'][1][level]['raw'])
        skill2_embed = util.quick_embed(f'Skill 2 - {skill2_name}', '')
        for item in skill2_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']
                
            skill2_embed.description += format_skilldesc(complete) + "\n"

        skill2_upload = discord.File(f'img\icon_skill2.png', filename='skill2.png')
        skill2_embed.set_thumbnail(url='attachment://skill2.png')

        skill2_embed.add_field(name="Type", value=f"{nikke['skills'][1]['type']}", inline=True)
        skill2_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][1]['cooldown'] is None else str(nikke['skills'][1]['cooldown']) + ' seconds'}", inline=True)

        # BURST

        burst_data = json.loads(nikke['skills'][2][level]['raw'])
        burst_embed = util.quick_embed(f'Burst - {burst_name}', '')
        for item in burst_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']
                
            burst_embed.description += format_skilldesc(complete) + "\n"

        burst_upload = discord.File(f'img\icon_burst.png', filename='burst.png')
        burst_embed.set_thumbnail(url='attachment://burst.png')

        burst_embed.add_field(name="Type", value=f"{nikke['skills'][2]['type']}", inline=True)
        burst_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][2]['cooldown'] is None else str(nikke['skills'][2]['cooldown']) + ' seconds'}", inline=True)

        await asyncio.sleep(4)
        await itcn.followup.send(embeds=[embed, normal_embed, skill1_embed, skill2_embed, burst_embed], files=[sight_upload, skill1_upload, skill2_upload, burst_upload])