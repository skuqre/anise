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
            "Always fun to see things explode. If you've got a rocket launcher, what else are you supposed to do?",
            "The fridge? Still has soda. Lots of em. Commander looks like he doesn't really abide by it though...",
            "It's been 25 days since Modernia came, we've been teaching her and... I think we need another reset...",
            "Modernia shook all my cans of soda... The Commander and I had to clean it all up. Was a flood in there.",
            "What's with the \"é\" in my name? Felt like it. Nothing much going on when it's just \"Anis\". Make yourself unique for once!",
            "Rapture this.. rapture that... why don't you (Inappropriate language detected. Rest of message has been filtered out.)",
            "Firepower! What do you mean I don't say that? I'm definitely Anis!",
            "This is Rapi. What is this all about? Who are you people?",
            "Guns n Roses make the world go round... Think of a better duo if you feel so inclined.",
            "Sometimes, I wonder; why did the manufacturers make us... like this? We could've been plain as all hell, y'know?",
            "Despite everything, the Commander still gets out alive in our missions. We're doing a good job!",
            "Do you know why the Commander has those certain type of magazines...?",
            "Dissipated a Rapture today. Like, totally made it dematerialize. Nothing was left of it anymore.",
            "I uhh... spilt more soda than usual. Oops."
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
            "(Inappropriate language detected. Prediction filtered.)",
            "Think about it deeply, and try again.",
            "It is unknown what will occur in the end."
        ]

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

        \- skuqre#7660
        """

        await itcn.send(embed=util.quick_embed('Sorry!', text.strip()))


def setup(bot: cmds.Bot) -> None:
    bot.add_cog(ExtraCommands(bot))
    print("Extra commands loaded!")
