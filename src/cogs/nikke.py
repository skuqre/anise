import os
import json
import disnake
import aiohttp
import requests
import src.util as util
from thefuzz import process
from disnake.ext import commands as cmds
from datetime import datetime, timezone


def format_skilldesc(desc: str):
    tor = desc.strip()
    if ":" in desc:
        tor = "**" + tor.replace(":", "**:")
    elif desc.startswith('■'):
        tor = "**" + tor + "**"
    else:
        tor = tor
    return tor


class NikkeCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot
        self.advisechars : list[str] = []
        self.charslugs : list[str] = {
            "prydwen": [],
            "nikkegg": []
        }
        self.charnames : dict[str, str] = {}
        self.init_charslugs();
        self.list_advisechars()

    # Request NIKKE data.
    async def request_nikke(self, character: str, nikke_gg: bool = False):
        try:
            async with aiohttp.ClientSession() as session:
                data = None
                if not nikke_gg:
                    data = await session.get(f'https://www.prydwen.gg/page-data/nikke/characters/{util.kebab(character)}/page-data.json')
                else:
                    data = await session.get(f'https://api.dotgg.gg/nikke/character/{util.kebab(character)}')
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
        
    def list_advisechars(self):
        maxlen = 0
        if os.path.exists("local/advise.json"):
            adviselist = json.loads(open("local/advise.json", "r").read())
            for adv in adviselist['data']:
                if adv.get('nikke') and not (adv.get('nikke') in self.advisechars):
                    self.advisechars.append(adv['nikke'])

                if len(adv.get('goodanswer')) > maxlen:
                    maxlen = len(adv.get('goodanswer'))
                if len(adv.get('badanswer')) > maxlen:
                    maxlen = len(adv.get('badanswer'))
        else:
            print("!!WARNING!! : No advise cache saved; please run the Advise lookup command atleast once for the autocomplete to function.")

    def save_advise(self, data):
        new_shit = {
            "data": data,
            "anise_LastUpdate": datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
        }

        to_save = json.dumps(new_shit, indent=4)

        os.makedirs('local', exist_ok=True)

        with open('local/advise.json', mode='w+') as f:
            f.write(to_save)

        self.list_advisechars()
        self.init_charslugs();
    
    def init_charslugs(self):
        prydwen_r = requests.get("https://www.prydwen.gg/page-data/nikke/characters/page-data.json").json()
        prydwen_chars = prydwen_r['result']['data']['allCharacters']['nodes']

        for char in prydwen_chars:
            self.charslugs['prydwen'].append(char['slug'])
            self.charnames[char['slug']] = char['name']

        nikkegg_r = requests.get("https://api.dotgg.gg/nikke/characters").json()
        for char in nikkegg_r:
            self.charslugs['nikkegg'].append(char['url'])


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
            embed = util.quick_embed('Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
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

        burst = util.emotes['burst' + nikke['burstType']]

        if (character in util.any_burst_nikkes):
            burst = util.emotes['burstA']

        # Combat
        combat = f"""
        **Rarity**: {util.emotes[nikke['rarity'].lower()]}
        **Class**: {nikke['class']}
        **Weapon**: {nikke['weapon']}
        **Element**: {nikke['element']}
        **Burst Type**: {burst}
        """
        embed.add_field(name="Combat", value=combat.strip(), inline=True)

        prydwen_upload = disnake.File(f'img\dbicons\prydwen.png', filename='prydwen.png')
        embed.set_footer(text="Data from https://www.prydwen.gg! Go visit!", icon_url='attachment://prydwen.png')

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

        await itcn.send(embed=embed, ephemeral=only_to_you, files=[prydwen_upload])

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

        sight_upload = disnake.File(f'img\sights\{sight}.png', filename='sight.png')
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

        skill1_upload = disnake.File(f'img\icon_skill1.png', filename='skill1.png')
        skill1_embed.set_thumbnail(url='attachment://skill1.png')

        skill1_embed.add_field(name="Type", value=f"{nikke['skills'][0]['type']}", inline=True)
        skill1_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][0]['cooldown'] is None else str(nikke['skills'][0]['cooldown']) + ' seconds'}", inline=True)

        # SKILL 2

        skill2_data = json.loads(nikke['skills'][1][level]['raw'])
        skill2_embed = util.quick_embed(skill2_name, '')
        skill2_embed.set_author(name='Skill 2')
        for item in skill2_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            skill2_embed.description += format_skilldesc(complete) + "\n"

        skill2_upload = disnake.File(f'img\icon_skill2.png', filename='skill2.png')
        skill2_embed.set_thumbnail(url='attachment://skill2.png')

        skill2_embed.add_field(name="Type", value=f"{nikke['skills'][1]['type']}", inline=True)
        skill2_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][1]['cooldown'] is None else str(nikke['skills'][1]['cooldown']) + ' seconds'}", inline=True)

        # BURST

        burst_data = json.loads(nikke['skills'][2][level]['raw'])
        burst_embed = util.quick_embed(burst_name, '')
        burst_embed.set_author(name='Burst')
        for item in burst_data['content']:
            complete = ''

            for node in item['content']:
                complete += node['value']

            burst_embed.description += format_skilldesc(complete) + "\n"

        burst_upload = disnake.File(f'img\icon_burst.png', filename='burst.png')
        burst_embed.set_thumbnail(url='attachment://burst.png')

        burst_embed.add_field(name="Type", value=f"{nikke['skills'][2]['type']}", inline=True)
        burst_embed.add_field(name="Cooldown", value=f"{'None' if nikke['skills'][2]['cooldown'] is None else str(nikke['skills'][2]['cooldown']) + ' seconds'}", inline=True)

        await itcn.send(embeds=[embed, normal_embed, skill1_embed, skill2_embed, burst_embed], files=[sight_upload, skill1_upload, skill2_upload, burst_upload], ephemeral=only_to_you)

    @nikke.sub_command(name='image', description='Display NIKKE character images. 3 types included.')
    async def image(self, itcn: disnake.CommandInteraction, character: str, type: str = cmds.Param(choices=["Head Bust", "Full Body"], description="Image type to send.")):
        await itcn.response.defer(with_message=True)
        data_gg = await self.request_nikke(character, nikke_gg=True)

        if data_gg is None:
            embed = util.quick_embed(
                'Uh oh!', 'Huh, looks like an exception occurred. Try again?', 0xff3d33)
            await itcn.send(embed=embed)
            return

        embed = util.quick_embed('', '')
        embed.title = data_gg['name']

        url = ''

        match type:
            case "Full Body":
                url = 'https://static.dotgg.gg/nikke/characters/' + data_gg['imgBig'] + '.png'
                embed.set_author(name="Full Body Image")
            # case "Card Bust":
            #     url = 'https://www.prydwen.gg' + nikke['cardImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src']
                # embed.set_author(name="Card Bust Image")
            case "Head Bust":
                url = 'https://static.dotgg.gg/nikke/characters/' + data_gg['img'] + '.png'
                embed.set_author(name="Head Bust Image")

        embed.set_image(url=url)

        await itcn.send(embed=embed)

    @info.autocomplete("character")
    @skills.autocomplete("character")
    def pryd_autocomplete(self, itcn: disnake.CommandInteraction, string: str):
        string = string.lower()
        if len(string) <= 0:
            return []
        results = [char for char in self.charslugs['prydwen'] if string in char.lower()]
        return results if len(results) <= 25 else []
    
    @image.autocomplete("character")
    def nkgg_autocomplete(self, itcn: disnake.CommandInteraction, string: str):
        string = string.lower()
        if len(string) <= 0:
            return []
        results = [char for char in self.charslugs['nikkegg'] if string in char.lower()]
        return results if len(results) <= 25 else []

    @nikke.sub_command(name='advise', description='Advise search. Character is optional.')
    async def advise(self, itcn: disnake.CommandInteraction, query: str, character: str = None, update_cache: bool = False):
        await itcn.response.defer(with_message=True)

        embed = util.quick_embed('', '')
        embed.title = "📝 Results"
        embed.description = "+100 bond answers are marked with a 🟩.\n+50 bond answers are marked with a 🟥.\nResults with **Missing** may have their questions/answers include the character's name.\nSome Nikkes may have different names (e.g. Hongryeon for Scarlet) so be wary of your Nikke's lore!\n\n"

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

            name = k

            if k != 'Monologue' and k != 'Missing':
                name = self.charnames[(k if not (k in util.weirdfilter) else util.weirdfilter[k])]

            for v in v1:
                v[0] = v[0].replace('\n', ' ')
                v[1] = v[1].replace('\n', ' ')
                v[2] = v[2].replace('\n', ' ')

                embed.description += f"""> **{name}**: _{v[0]}_
                > 🟩 {v[1]}
                > 🟥 {v[2]}

                """
                amount += 1

        nikkegg_upload = disnake.File(f'img\dbicons\\nikkegg.png', filename='nikkegg.png')
        embed.description = embed.description.replace("{AccountData.NickName}", "`[YOUR-NAME]`")

        if len(embed.description) > 4096:
            embed.title = 'Uh oh!'
            embed.description = 'Your query is too broad. Mind putting more into it?'
        elif amount == 0:
            embed.description = 'No results found... Check again!\n\n**Protip**: If the query has a Nikkes name in it, I recommend you to NOT fill the character field for a more broad search.'
        else:
            embed.set_footer(text=f"Data from https://nikke.gg! Go visit! | Last updated: {date + ' (UTC)' if not update_cache else 'Just now'}", icon_url='attachment://nikkegg.png')
            await itcn.send(embed=embed, files=[nikkegg_upload])
            return

        await itcn.send(embed=embed)

    @advise.autocomplete("character")
    def advise_autocomplete(self, itcn: disnake.CommandInteraction, string: str):
        string = string.lower()
        if len(string) <= 0:
            return []
        results = [char for char in self.advisechars if string in char.lower()]
        return results if len(results) <= 25 else []
    
    # Worst code ever?
    # Kill yourself?
    @nikke.sub_command(name='tierlist', description='Tierlist search for both NIKKE.GG and Prydwen.')
    async def tierlist(self, itcn: disnake.CommandInteraction, character: str):
        await itcn.response.defer(with_message=True)

        embed_nikkegg = util.quick_embed('', '')
        embed_prydwen = util.quick_embed('', '')

        char_nikkegg = process.extractOne(character, self.charslugs['nikkegg'])[0]
        data_nikkegg = await self.request_nikke(char_nikkegg, nikke_gg=True)

        embed_nikkegg.add_field(name="Combined*", value=f"**{util.nikke_gg_ratings(data_nikkegg['tierlist']['Combined'])}** ({data_nikkegg['tierlist']['Combined']})", inline=False)
        embed_nikkegg.add_field(name="Story", value=f"**{util.nikke_gg_ratings(data_nikkegg['tierlist']['Story'])}** ({data_nikkegg['tierlist']['Story']})", inline=True)
        embed_nikkegg.add_field(name="Boss", value=f"**{util.nikke_gg_ratings(data_nikkegg['tierlist']['Boss'])}** ({data_nikkegg['tierlist']['Boss']})", inline=True)
        embed_nikkegg.add_field(name="PvP", value=f"**{util.nikke_gg_ratings(data_nikkegg['tierlist']['PvP'])}** ({data_nikkegg['tierlist']['PvP']})", inline=True)

        char_prydwen = process.extractOne(character, self.charslugs['prydwen'])[0]
        data_prydwen = await self.request_nikke(char_prydwen)
        nikke_prydwen = data_prydwen['result']['data']['currentUnit']['nodes'][0]

        embed_prydwen.add_field(name="Story (Early)", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['storyEarly']]}** ({(int(nikke_prydwen['ratings']['storyEarly']) / 11 * 10):.1f})", inline=True)
        embed_prydwen.add_field(name="Story (Mid)", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['storyMid']]}** ({(int(nikke_prydwen['ratings']['storyMid']) / 11 * 10):.1f})", inline=True)
        embed_prydwen.add_field(name="Story (Late)", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['storyEnd']]}** ({(int(nikke_prydwen['ratings']['storyEnd']) / 11 * 10):.1f})", inline=True)
        embed_prydwen.add_field(name="Boss (Solo)", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['bossSolo']]}** ({(int(nikke_prydwen['ratings']['bossSolo']) / 11 * 10):.1f})", inline=True)
        embed_prydwen.add_field(name="Boss (Adds)", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['bossAdds']]}** ({(int(nikke_prydwen['ratings']['bossAdds']) / 11 * 10):.1f})", inline=True)
        embed_prydwen.add_field(name="PvP", value=f"**{util.prydwen_ratings[nikke_prydwen['ratings']['pvp']]}** ({(int(nikke_prydwen['ratings']['pvp']) / 11 * 10):.1f})", inline=True)

        embed_nikkegg.set_thumbnail(url='https://www.prydwen.gg' + nikke_prydwen['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])
        embed_prydwen.set_thumbnail(url='https://www.prydwen.gg' + nikke_prydwen['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])

        embed_nikkegg.title = data_nikkegg['name']
        embed_prydwen.title = nikke_prydwen['name']

        nikkegg_upload = disnake.File(f'img\dbicons\\nikkegg.png', filename='nikkegg.png')
        embed_nikkegg.set_author(name="Nikke.gg", icon_url='attachment://nikkegg.png')

        prydwen_upload = disnake.File(f'img\dbicons\prydwen.png', filename='prydwen.png')
        embed_prydwen.set_author(name="Prydwen Institute", icon_url='attachment://prydwen.png')

        embed_nikkegg.set_footer(text='*may be rounded')
        embed_prydwen.set_footer(text='There are no numerical ratings from Prydwen.')

        await itcn.send(embeds=[embed_nikkegg, embed_prydwen], files=[nikkegg_upload, prydwen_upload])

    @tierlist.autocomplete("character")
    def general_autocomplete(self, itcn: disnake.CommandInteraction, string: str):
        string = string.lower()
        if len(string) <= 0:
            return []
        
        results = [char for char in self.charslugs['nikkegg'] + self.charslugs['prydwen'] if string in char.lower()]
        return results if len(results) <= 25 else []


def setup(bot: cmds.Bot) -> None:
    bot.add_cog(NikkeCommands(bot))
    print("NIKKE commands loaded!")