# CtrlBot

Open-source code of my Discord bot.

This is just a fun personal project of mine, nothing too serious.

It will be all written in <b>Python</b> (as this is the programming language required by my college), however I do plan to make a different version of this in the future in another programming language. 


## Bot Features:
- Dynamic VC Creation: You can use */setup-vc-panel [text_channel] [voice_channel]*, where "text_channel" is there you want the panel to be in and "voice_channel" is where you want users to join to create a new VC. This means that, with just 1 voice channel, your members can make an infinite amount of VCs when needed. The owner of the VC can customize it via the panel and once everyone leaves the VC will delete itself.
- Ticket System: You can use */setup-ticket-panel [text_channel] [support_role]*, where "text_channel" is where you want the panel to be in and "support_role" is the role you want to be able to view active tickets. The ticket can then only be seen by members with "administrator" privileges or members with the "support role" (The individual who made the ticket can also see their own ticket, obviously). A member can have up to 1 active ticket at a time, meaning that they cannot flood the server with channels. Upon closing a ticket (with our without a reason), the bot will send a DM to the creator of the ticket saying who it was closed by and the reason it was closed. This will include a date stamp of when it was closed as the user can see when the message was sent to them.
- Adding / Removing Roles: There are 4 main commands for this: */give-role-all [role]* , */remove-role-all [role]* , */role [user] [role]* , */role-remove [user] [role]*. Fairly straight forward what this does, therefore I will not go into too much detail. One thing worth mentioning is that if you want the bot to remove/add a role, the @CtrlBot role must be placed above that role, otherwise it will not have permission to add/remove that role.
- Banning / Kicking Users: You can use */ban [user] [optional: reason]* and */kick [user] [optional: reason]* if you do not wish to directly grant staff members the option to ban/kick members directly.

## Future Plans / Additions:
- Chat Levelling System: Some sort of system which gives users XP for chatting and allows them to level up. The XP requirement per level will exponentially grow (therefore there will not be a maximum level, however it will be harder and harder to level up). Levels can then be linked to rewards (i.e assigning a new role).
- Bot Settings Panel: Simple panel for administrators to use in order to manage the bot. (i.e change staff-command roles). Will be fairly simple, it will just help be removing the need of having "administrator" privileges to use the commands.
- Currency / Gambling System: Everyone loves money, and everyone surely loves gambling. I plan to add a system with a daily money reward, some sort of gambling system (blackjack, coin flip etc.) and perhaps allow staff to set-up a role reward once someone reaches X money.
- Suggestion System: */suggest-channel [text_channel* and ]*/suggest [suggestion]*. This will allow staff to setup a suggestions channel where suggestions will be sent and */suggest* can be used by all users to create suggestions which can be Accepted/Denied by staff members. There will be a cooldown in order to avoid spamming. Each suggestion will have a Thread created in order for members to discuss their opinion on this suggestion.
