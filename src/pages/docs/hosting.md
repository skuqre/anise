---
layout: ../../layouts/DocsLayout.astro
title: Hosting
---

# Hosting
As funny as it is, **Anisé isn't publicly hosted**. Probably will never be. So you may have to host your own Anisé every once in a while (that's how I use the bot anyway, lol!).

Below includes a nasty, hasty-pasted, small tutorial on how to host your own Anisé.

## Create a Bot
Create an application on [discord.com/developers](https://discord.com/developers). Click the big blurple button that says "New Application", which should just be on the top-right of the page.

![](../images/docs/discord_newapplication.png)

Put in the name of your choice, and head to the Bot section of your application's page.

Be sure to invite your bot to your server. A tab named "URL Generator" in the side bar of the application's page should help you. Click the checkbox `bot` to generate an invite URL for your bot.

Get your token, and get yourself the [source code of Anisé](https://github.com/skuqre/anise). Should be easy to download.

Rename `.env.example` to just `.env`. Edit the file in Notepad, and replace `TOKEN` with your bot's token. Should be a long line of random letters and numbers.
<div class="codeblock">
<pre><code>
bot_secret=A_REALLY_LONG_STRING_OF_LETTERS_SYMBOLS_AND_NUMBERS
is_debug=False
</code></pre>
</div>

> The other line (`is_debug`) is something used for developer shenanigans! If it's `True`, the bot will automatically reload when a file from `src/cogs` has been changed. Useful if you want immediate results when creating a command for Anisé.

After everything is set; click `run.bat`. When it says "Hello chat.", everything should be fine.