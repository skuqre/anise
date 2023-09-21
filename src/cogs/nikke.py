import os
import json
import disnake
import aiohttp
import src.util as util
from disnake.ext import commands as cmds
from datetime import datetime, timezone


def format_skilldesc(desc: str):
    tor = desc.strip()
    if ":" in desc:
        tor = "**" + tor.replace(":", "**:")
    elif desc.startswith('■'):
        return tor
    else:
        tor = "**" + tor + "**"
    return tor


class NikkeCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot
        self.advisechars : list[str] = []

        if os.path.exists("local/advise.json"):
            adviselist = json.loads(open("local/advise.json", "r").read())
            for adv in adviselist['data']:
                if adv.get('nikke') and not (adv.get('nikke') in self.advisechars):
                    self.advisechars.append(adv['nikke'])

            print("ADVISE CHARACTERS: ", self.advisechars)
        else:
            print("!!WARNING!! : No advise cache saved; please run the Advise lookup command atleast once for the autocomplete to function.")



    # Request NIKKE data.
    async def request_nikke(self, character: str):
        try:
            async with aiohttp.ClientSession() as session:
                data = await session.get(f'https://www.prydwen.gg/page-data/nikke/characters/{util.kebab(character)}/page-data.json')
                return await data.json()
        except:
            return None

    async def request_advise(self):
        try:
            async with aiohttp.ClientSession() as session:
                data = await session.get(f'https://api.dotgg.gg/nikke/advise')
                return await data.json()
        except:
            return None

    def save_advise(self, data):
        new_shit = {
            "data": data,
            "anise_LastUpdate": datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
        }

        to_save = json.dumps(new_shit, indent=4)

        os.makedirs('local', exist_ok=True)

        with open('local/advise.json', mode='w+') as f:
            f.write(to_save)

    @cmds.slash_command(name='nikkepedia')
    async def nikke(self, itcn: disnake.CommandInteraction):
        pass  # This command doesn't do anything, and somehow can't be invoked.

    @nikke.sub_command(name='what', description='What is NIKKE?')
    async def what(self, itcn: disnake.CommandInteraction):
        what = """
        **How I (the great Anisé), would describe NIKKE?**

        Goddess of Victory: NIKKE is a third-person shooter game made by
        SHIFT UP and Level Infinite for Android and IOS, and even for Windows.

        Players assume the role of a Commander, who controls 5 of the titular
        Nikkes to fight against the Raptures, the common enemy of the game.

        Gameplay includes a one-handed experience, quick switching between Nikkes, 
        with the "one-handed" part being the core of it. You can even let the game
        play by itself!
        """

        embed = util.quick_embed("What is NIKKE?", what.strip())
        embed.set_image(url='https://haxeflixel.is-terrible.com/64JSQlQc0.png')
        await itcn.send(embed=embed)

    @nikke.sub_command(name='whois', description='Who is this NIKKE? Character name must be in kebab-case.')
    async def info(self, itcn: disnake.CommandInteraction, character: str, only_to_you: bool = True):
        await itcn.response.defer(with_message=True, ephemeral=only_to_you)
        data = await self.request_nikke(character)

        if data is None:
            embed = util.quick_embed(
                'Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await itcn.send(embed=embed, ephemeral=only_to_you)
            return

        nikke = data['result']['data']['currentUnit']['nodes'][0]

        embed = util.quick_embed('', '')
        embed.title = nikke['name']

        if not nikke['backstory'] is None:
            embed.description = nikke['backstory']['backstory'] + '\n'

        embed.set_thumbnail(url='https://www.prydwen.gg' +
                            nikke['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

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
        **VA (:flag_us:/:flag_gb:)**: {nikke['cv']['en']}
        """
        embed.add_field(name="Miscellaneous", value=misc.strip(), inline=False)

        if not nikke['specialities'] is None:
            embed.add_field(name="Specialities", value='\n'.join(
                nikke['specialities']), inline=True)

        await itcn.send(embed=embed, ephemeral=only_to_you)

    @nikke.sub_command(name='skills', description='What can this NIKKE do? Character name must be in kebab-case.')
    async def skills(self, itcn: disnake.CommandInteraction, character: str, max_level: bool = False, only_to_you: bool = True):
        await itcn.response.defer(with_message=True, ephemeral=only_to_you)
        data = await self.request_nikke(character)

        if data is None:
            embed = util.quick_embed(
                'Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await itcn.send(embed=embed, ephemeral=only_to_you)
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
        embed.set_thumbnail(url='https://www.prydwen.gg' +
                            nikke['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        # NORMAL ATTACK

        normal_data = json.loads(nikke['basicAttack']['raw'])
        normal_embed = util.quick_embed(nikke['weapon'], '')
        normal_embed.set_author(name='Normal Attack')
        for item in normal_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            normal_embed.description += format_skilldesc(complete) + "\n"

        normal_embed.add_field(name="Control Type",
                               value=f"{nikke['controlMode']}", inline=True)
        normal_embed.add_field(
            name="Capacity", value=f"{nikke['ammoCapacity']} ammo", inline=True)
        normal_embed.add_field(
            name="Reload Time", value=f"{nikke['reloadTime']} seconds", inline=True)

        sight_upload = disnake.File(
            f'img\sights\{sight}.png', filename='sight.png')
        normal_embed.set_thumbnail(url='attachment://sight.png')

        # SKILL 1

        skill1_data = json.loads(nikke['skills'][0][level]['raw'])
        skill1_embed = util.quick_embed(skill1_name, '')
        skill1_embed.set_author(name='Skill 1')
        for item in skill1_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            skill1_embed.description += format_skilldesc(complete) + "\n"

        skill1_upload = disnake.File(
            f'img\icon_skill1.png', filename='skill1.png')
        skill1_embed.set_thumbnail(url='attachment://skill1.png')

        skill1_embed.add_field(
            name="Type", value=f"{nikke['skills'][0]['type']}", inline=True)
        skill1_embed.add_field(
            name="Cooldown", value=f"{'None' if nikke['skills'][0]['cooldown'] is None else str(nikke['skills'][0]['cooldown']) + ' seconds'}", inline=True)

        # SKILL 2

        skill2_data = json.loads(nikke['skills'][1][level]['raw'])
        skill2_embed = util.quick_embed(skill2_name, '')
        skill2_embed.set_author(name='Skill 2')
        for item in skill2_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            skill2_embed.description += format_skilldesc(complete) + "\n"

        skill2_upload = disnake.File(
            f'img\icon_skill2.png', filename='skill2.png')
        skill2_embed.set_thumbnail(url='attachment://skill2.png')

        skill2_embed.add_field(
            name="Type", value=f"{nikke['skills'][1]['type']}", inline=True)
        skill2_embed.add_field(
            name="Cooldown", value=f"{'None' if nikke['skills'][1]['cooldown'] is None else str(nikke['skills'][1]['cooldown']) + ' seconds'}", inline=True)

        # BURST

        burst_data = json.loads(nikke['skills'][2][level]['raw'])
        burst_embed = util.quick_embed(burst_name, '')
        burst_embed.set_author(name='Burst')
        for item in burst_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            burst_embed.description += format_skilldesc(complete) + "\n"

        burst_upload = disnake.File(
            f'img\icon_burst.png', filename='burst.png')
        burst_embed.set_thumbnail(url='attachment://burst.png')

        burst_embed.add_field(
            name="Type", value=f"{nikke['skills'][2]['type']}", inline=True)
        burst_embed.add_field(
            name="Cooldown", value=f"{'None' if nikke['skills'][2]['cooldown'] is None else str(nikke['skills'][2]['cooldown']) + ' seconds'}", inline=True)

        await itcn.send(embeds=[embed, normal_embed, skill1_embed, skill2_embed, burst_embed], files=[sight_upload, skill1_upload, skill2_upload, burst_upload], ephemeral=only_to_you)

    @nikke.sub_command(name='image', description='Display NIKKE character images. 3 types included.')
    async def image(self, itcn: disnake.CommandInteraction, character: str, type: str = cmds.Param(choices=["Head Bust", "Card Bust", "Full Body"], description="Image type to send.")):
        await itcn.response.defer(with_message=True)
        data = await self.request_nikke(character)

        if data is None:
            embed = util.quick_embed(
                'Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await itcn.send(embed=embed)
            return

        nikke = data['result']['data']['currentUnit']['nodes'][0]

        embed = util.quick_embed('', '')
        embed.title = nikke['name']

        imageType = 'smallImage'

        match type:
            case "Full Body":
                imageType = 'fullImage'
                embed.set_author(name="Full Body Image")
            case "Card Bust":
                imageType = 'cardImage'
                embed.set_author(name="Card Bust Image")
            case "Head Bust":
                imageType = 'smallImage'
                embed.set_author(name="Head Bust Image")

        embed.set_image(url='https://www.prydwen.gg' +
                        nikke[imageType]['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        await itcn.send(embed=embed)

    @nikke.sub_command(name='advise', description='Advise search. Character is optional.')
    async def advise(self, itcn: disnake.CommandInteraction, query: str, character: str = None, update_cache: bool = False):
        await itcn.response.defer(with_message=True)

        embed = util.quick_embed('', '')
        embed.title = "Results"
        embed.description = "+100 bond answers are marked with a :green_square:.\n+50 bond answers are marked with a :red_square:.\nResults with `Missing` may have their questions/answers include the character's name.\nSome Nikkes may have different names (e.g. Hongreyon for Scarlet) so be wary of your Nikke's lore!\n\n"

        data = None
        date = None

        if update_cache:
            data = await self.request_advise()
            self.save_advise(data=data)
        else:
            huh = json.loads(open("local/advise.json", "r").read())
            data = huh.get('data')
            date = huh.get('anise_LastUpdate')

        results = {}

        for item in data:
            to = 'Missing'

            if item.get('nikke'):
                to = item['nikke']

            if results.get(to) is None:
                results[to] = []

            check = [item['question'], item['goodanswer'], item['badanswer']]
            for shit in check:
                if query.lower() in shit.lower():
                    results[to].append(
                        [item['question'], item['goodanswer'], item['badanswer']])
                    break

        amount = 0
        for k, v1 in results.items():
            if not (character is None):
                if not (character in k):
                    continue

            for v in v1:
                embed.description += f"""**{k}**: {v[0]}
                :green_square: `{v[1]}`
                :red_square: `{v[2]}`

                """
                amount += 1

        if len(embed.description) > 4096:
            embed.title = 'Uh oh!'
            embed.description = 'Your query is too broad. Mind putting more into it?'
        elif amount == 0:
            embed.description = 'No results found... Check again!\n\n**Protip**: If the query has a Nikkes name in it, I recommend you to NOT fill the character field for a more broad search.'
        else:
            embed.set_footer(
                text=f"Last updated: {date + ' (UTC)' if not update_cache else 'Just now'} | Data from https://dotgg.gg. Go visit!")

        await itcn.send(embed=embed)

    @advise.autocomplete("character")
    def char_autocomplete(self, itcn: disnake.CommandInteraction, string: str):
        string = string.lower()
        return [char for char in self.advisechars if string in char.lower()]


def setup(bot: cmds.Bot) -> None:
    bot.add_cog(NikkeCommands(bot))
    print("NIKKE commands loaded!")