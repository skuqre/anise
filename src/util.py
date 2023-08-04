from re import sub
import disnake


def kebab(s):
    return '-'.join(sub(r"(\s|_|-)+", " ", sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+", lambda mo: ' ' + mo.group(0).lower(), s)).split())


def quick_embed(title: str, desc: str, color: int = 0xf4d259):
    embed = disnake.Embed()
    embed.title = title
    embed.description = desc
    embed.color = color
    return embed
