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

def truncate_string(string: str, length: int):
    if len(string) <= length:
        return string
    else:
        return string[:length - 3].strip() + "..."
    
emotes = {
    "burst1": "<:burst1:1154461312378732634>",
    "burst2": "<:burst2:1154461316279455805>",
    "burst3": "<:burst3:1154461320293388288>",
    "ssr" : "<:os:1154464434505384067><:os:1154464434505384067><:or:1154464430814417026>",
    "sr" : "<:ps:1154464442772361267><:pr:1154464438947156029>",
    "r" : "<:br:1154464426318110813>"
}