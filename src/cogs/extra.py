import disnake
import src.util as util
from random import Random as Rnd
from disnake.ext import commands as cmds


class ExtraCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot: cmds.Bot = bot
        self.somethings: list[str] = [
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
            "Despite everything, the Commander still gets out alive in our missions. We're doing a good job!"
        ]

    @cmds.slash_command(name='shedidntsaythat', description="Let me spout out random stuff!")
    async def random(self, itcn: disnake.CommandInteraction):
        await itcn.send(content=Rnd().choice(self.somethings))


def setup(bot: cmds.Bot) -> None:
    bot.add_cog(ExtraCommands(bot))
    print("Extra commands loaded!")
