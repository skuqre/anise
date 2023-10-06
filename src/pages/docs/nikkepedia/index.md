---
layout: ../../../layouts/DocsLayout.astro
title: Nikkepedia
---

# Nikkepedia

A bunch of commands that interact with external databases.

Most commands are in the form `/nikkepedia <command>` for ease of access.

| Subcommand | Usage Example | Description |
| --- | --- | --- |
| [what](/anise/docs/nikkepedia/what) | `/nikkepedia what` | Returns a small description of Goddess of Victory: NIKKE from the eyes of Anisé. |
| [whois](/anise/docs/nikkepedia/whois) | `/nikkepedia whois <character> [only-to-you]` | Returns with a small description of the character in question. Skills excluded. |
| [skills](/anise/docs/nikkepedia/skills) | `/nikkepedia skills <character> [max-level-stats] [only-to-you]` | Returns with the skill descriptions of the character in question. Setting `[max-level-stats]` to `True` will return with skill descriptions at Level 10. |
| [image](/anise/docs/nikkepedia/image) | `/nikkepedia image <character> <type>` | Returns with an image of the character in question. `<type>` can only be **Head Bust**, **Card Bust**, or **Full Body**. |
| [advise](/anise/docs/nikkepedia/advise) | `/nikkepedia advise <query> [character] [update-cache]` | Advise lookup. **If this command has never been ran once, `[update-cache]` must be True. A warning in the terminal is given out if this is the case.** The `[character]` field has auto-completion. |

Commands with an `[only-to-you]` argument has this argument always default to **True** to prevent chat clutter; set it to **False** if you want to share the message with others.


If you'd like a more "in-depth" description for these commands (as these are summarizations) you can head to the left, they have their own unique page for descriptions.