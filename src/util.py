from re import sub
import disnake
import threading

emotes = {
    "burst1": "<:burst1:1154461312378732634>",
    "burst2": "<:burst2:1154461316279455805>",
    "burst3": "<:burst3:1154461320293388288>",
    "ssr": "<:os:1154464434505384067><:os:1154464434505384067><:or:1154464430814417026>",
    "sr": "<:ps:1154464442772361267><:pr:1154464438947156029>",
    "r": "<:br:1154464426318110813>"
}

weirdfilter = {
    'anis_s': 'sparkling-summer-anis',
    'helm_s': 'aqua-marine-helm',
    'neon_s': 'blue-ocean-neon',
    'mary_s': 'bay-goddess-mary',
    'marian_p': 'modernia',
    'rupee_w': 'winter-shopper-rupee',
    'anne': "miracle-fairy-anne",
    'snowwhite': 'snow-white',
    'hongryeon': 'scarlet'
}

prydwen_ratings = {
    "11": "SSS",
    "10": "SS",
    "9": "S",
    "8": "A",
    "7": "B",
    "6": "C",
    "5": "D",
    "4": "F"
}

# May be inaccurate, needs more info from nikke.gg lol!


def nikke_gg_ratings(num: float):
    ratings = {
        "SSS": num > 9.5 and num <= 10.0,
        "SS": num > 9.0 and num <= 9.5,
        "S+": num > 7.0 and num <= 9.0,
        "A": num > 6.0 and num <= 7.0,
        "B": num > 5.0 and num <= 6.0,
        "C": num > 4.0 and num <= 5.0,
        "D": num > 2.0 and num <= 4.0,
        "F": num <= 2.0
    }

    return list(ratings.keys())[list(ratings.values()).index(True)]


def kebab(s):
    # return '-'.join(sub(r"(\s|_|-)+", " ", sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+", lambda mo: ' ' + mo.group(0).lower(), s)).split())
    return s


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