---
layout: ../../../layouts/DocsLayout.astro
---

# advise

`/nikkepedia advise <query> [character] [update-cache]`

Search for advise answers through [nikke.gg](https://nikke.gg)'s advise list.

> I myself hope that this is an easier way to look it up, as I just have an awful experience with that page; even the dotgg one is an awful experience, and the nikke.gg one is just one large table.

It is recommended that you make your search less broad and more specific! Too broad and the command will refrain from showing the results. Even so, results that are too broad *may* give you a harder time finding the question you want.

---

### Arguments

| Argument | Possible values | Description | Optional |
| --- | --- | --- | --- |
| query | any | Your search query. Don't make it too broad! | 🔴 |
| character | any word (autocompleted) | Name of the character. The only thing different about this argument from the others, however, is that this has **autocomplete**. | 🟢 |
| update-cache | `True` or `False` | Update the local cache. If this command has not been ran once, this must be **True**. A warning will be issued at the terminal if this is the case. | 🟢 |