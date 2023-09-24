import json
import aiohttp
import disnake
import src.util as util
from random import Random as Rnd
from disnake.ext import commands as cmds

class ExtraCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot
        self.thingsshesays: list[str] = [
            "Are you really playing a game if you let it play all by yourself? And the game can also be played with one hand?",
            "I use my hands for two things. One, to play the game, and two, to hold the Bible.",
            "The fridge? Still has soda. Lots of em. Commander looks like he doesn't really abide by it though...",
            "What's with the \"é\" in my name? Felt like it. Nothing much going on when it's just \"Anis\". Make yourself unique for once!",
            "Rapture this.. rapture that... why don't you (Inappropriate language detected. Rest of message has been filtered out.)",
            "Firepower! What do you mean I don't say that? I'm definitely Anis!",
            "This is Rapi. What is this all about? Who are you people?",
            "Sometimes, I wonder; why did the manufacturers make us... like this? We could've been plain as all hell, y'know?",
            "Despite everything, the Commander still gets out alive in our missions. We're doing a good job!",
            "Do you know why the Commander has those certain type of magazines...?",
            "Dissipated a Rapture today. Like, totally made it dematerialize. Nothing was left of it anymore.",
            "I uhh... spilt more soda than usual. Oops.",
            "Yeah, I said that one line about sex once. I still stand by it!",
            "How would one make my swimsuit? Three standard medical masks should be fine."
        ]

        self.ballyes: list[str] = [
            "Sure.",
            "Without a doubt.",
            "All outcomes are positive.",
            "All signs point to yes.",
            "Definitely.",
            "It is decidedly so.",
            "Yes."
        ]
        self.ballno: list[str] = [
            "No.",
            "Absolutely not.",
            "It's gonna make things worse.",
            "Don't count on it.",
            "Sources said no.",
            "Outcomes are awful.",
            "It's not good for the future."
        ]
        self.ballidk: list[str] = [
            "Don't know.",
            "Maybe. Maybe not.",
            "Can't predict right now.",
            "Sources are hazy. Try again.",
            "(Inappropriate language detected. Message filtered.)",
            "Think about it deeply, and try again.",
            "It is unknown what will occur in the end."
        ]

        # most videos uploaded by DexterousPotato
        # please check em out for more game OSTs, especially Nikke
        self.nikkeost = json.loads(open("data/ost.json", "r").read())

        # make song choices unique each time
        self.nikkeostcurrent = self.nikkeost.copy()

        # nikke.gg's advise data names nikkes differently
        # this hand made filter picks some of those names and
        # changes them to ones prydwen would enjoy
        # i'm sure i forgot some
        self.weirdfilter = {
            'anis_s' : 'sparkling-summer-anis',
            'helm_s' : 'aqua-marine-helm',
            'neon_s' : 'blue-ocean-neon',
            'mary_s' : 'bay-goddess-mary',
            'marian_p' : 'modernia',
            'rupee_w' : 'winter-shopper-rupee',
            'anne' : "miracle-fairy-anne",
            'snowwhite' : 'snow-white',
            'hongreyon' : 'scarlet'
        }

        self.aniseadvise = json.loads(open("data/loladvise.json", "r").read())

    # Request NIKKE data.
    async def request_nikke(self, character: str):
        try:
            async with aiohttp.ClientSession() as session:
                data = await session.get(f'https://www.prydwen.gg/page-data/nikke/characters/{util.kebab(character)}/page-data.json')
                return await data.json()
        except:
            return None

    @cmds.slash_command(name='shedidntsaythat', description="Let me spout out random stuff!")
    async def randomsays(self, itcn: disnake.CommandInteraction):
        await itcn.response.defer(with_message=True)
        chosen = Rnd().choice(self.thingsshesays)
        await itcn.send(content=chosen)

    @cmds.slash_command(name='8ball', description="My magic 8 ball! It's a novelty!")
    async def magic_8ball(self, itcn: disnake.CommandInteraction):
        await itcn.response.defer(with_message=True)

        rnd = Rnd()
        rndint = rnd.randint(1, 3)

        match rndint:
            case 1:
                await itcn.send(embed=util.quick_embed('🎱 8 Ball', rnd.choice(self.ballyes)))
            case 2:
                await itcn.send(embed=util.quick_embed('🎱 8 Ball', rnd.choice(self.ballno)))
            case 3:
                await itcn.send(embed=util.quick_embed('🎱 8 Ball', rnd.choice(self.ballidk)))

    @cmds.slash_command(name='nikkeost', description="Get a random song from my potentially long list of bangers. All for you!")
    async def nikke_ost(self, itcn: disnake.CommandInteraction):
        await itcn.response.defer(with_message=True)

        rnd = Rnd()
        pick = rnd.choice(self.nikkeostcurrent)

        embed = util.quick_embed("🎶 Random OST", "")
        embed.description = f"""
        ### {pick['name']}
        Link: *{pick['link']}*

        {'*' + pick['comment'] + '*' if len(pick['comment']) > 0 else ""}
        """.strip()

        vidid = pick['link'].removeprefix('https://youtu.be/').strip()
        embed.set_image(url=f'https://img.youtube.com/vi/{vidid}/maxresdefault.jpg')

        await itcn.send(embed=embed, components=[])

        self.nikkeostcurrent.remove(pick)
        if len(self.nikkeostcurrent) == 0:
            self.nikkeostcurrent = self.nikkeost.copy()

    @cmds.slash_command(name='bondpractice', description="Advise a random NIKKE. I'll be playing as her for you... No cheating!")
    async def random_bond(self, itcn: disnake.CommandInteraction, only_to_you: bool = True):
        await itcn.response.defer(with_message=True, ephemeral=only_to_you)

        embed = util.quick_embed('📝 Bond Practice', '')
        
        adviselist = json.loads(open("local/advise.json", "r").read())
        advises = adviselist['data']

        rnd = Rnd()
        pick = rnd.choice(advises)
        question = pick['question'].replace("{AccountData.NickName}", "[YOUR-NAME]")
        good_answer= pick['goodanswer'].replace("{AccountData.NickName}", "[YOUR-NAME]")
        bad_answer = pick['badanswer'].replace("{AccountData.NickName}", "[YOUR-NAME]")

        nikke = None
        if pick.get('nikke'):
            if pick['nikke'] != 'anise':
                data = await self.request_nikke(pick['nikke'] if not (pick['nikke'] in self.weirdfilter) else self.weirdfilter[pick['nikke']])
                nikke = data['result']['data']['currentUnit']['nodes'][0]
                embed.set_thumbnail(url='https://www.prydwen.gg' + nikke['smallImage']['localFile']['childImageSharp']['gatsbyImageData']['images']['fallback']['src'])
            else:
                pass
        else:
            nikke = {
                'name' : 'Monologue'
            }

        embed.description = f"""
        ### {nikke['name']}

        _"{question}"_
        """

        if len(good_answer) > 80:
            good_answer = util.truncate_string(good_answer, 80)
        if len(bad_answer) > 80:
            bad_answer = util.truncate_string(bad_answer, 80)

        good_button = disnake.ui.Button(label=good_answer, style=disnake.ButtonStyle.gray, custom_id="good")
        bad_button = disnake.ui.Button(label=bad_answer, style=disnake.ButtonStyle.gray, custom_id="bad")
        comps = [good_button, bad_button]
        rnd.shuffle(comps)

        await itcn.send(embed=embed, components=comps)


    
    @cmds.slash_command(name='ping', description="What's my latency?")
    async def pong(self, itcn: disnake.CommandInteraction):
        await itcn.send(embed=util.quick_embed('🏓 Pong!', f'**Bot latency**: {round(self.bot.latency * 1000, 2) }ms'))

    # Really just for officiality. 
    # You can remove this command if you're using Anisé as 
    # a base for your Discord bot and you want to go public.
    @cmds.slash_command(name='invite', description='---')
    async def invite(self, itcn: disnake.CommandInteraction):
        text = """
        Anisé is currently an **invite-only** Discord bot.
        Servers with Anisé in it have express permissions
        of from the owner of the server, or was just added in
        by the bot's developer (<@317204000250265600>).

        Though, thank you for expressing your interest
        for Anisé in your servers!

        \- skuqre
        """

        await itcn.send(embed=util.quick_embed('Sorry!', text.strip()))

    @cmds.Cog.listener()
    async def on_button_click(self, itcn: disnake.MessageInteraction):
        if itcn.component.custom_id in ['good', 'bad']:
            view = disnake.ui.View.from_message(itcn.message)
            for item in view.children:
                if isinstance(item, disnake.ui.Button):
                    if item.custom_id in ['good', 'bad']:
                        if item.custom_id == 'good':
                            item.style = disnake.ButtonStyle.success
                        if item.custom_id == 'bad':
                            item.style = disnake.ButtonStyle.danger
                            
                        item.disabled = True

            await itcn.response.defer()

            if itcn.component.custom_id == 'good':
                embed = util.quick_embed('📝 Bond Practice', 'You picked the right choice! Good job!\n\n+100 Bond', 0x77dd77)

                upload = disnake.File(f'img\icon_bond_up.png', filename='bond.png')
                embed.set_thumbnail(url='attachment://bond.png')

                await itcn.followup.edit_message(embeds=[embed], files=[upload], message_id=itcn.message.id, view=view)
            elif itcn.component.custom_id == 'bad':
                embed = util.quick_embed('📝 Bond Practice', 'Failure.\n\n+50 Bond', 0xff6961)

                upload = disnake.File(f'img\icon_bond_down.png', filename='bond.png')
                embed.set_thumbnail(url='attachment://bond.png')

                await itcn.followup.edit_message(embeds=[embed], files=[upload], message_id=itcn.message.id, view=view)



def setup(bot: cmds.Bot) -> None:
    bot.add_cog(ExtraCommands(bot))
    print("Extra commands loaded!")
