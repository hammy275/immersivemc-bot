from typing import Union
import discord
import sys
import re

import config

invite_regex: re.Pattern = re.compile(r"discord\.(gg/|com/invite)")
link_regex: re.Pattern = re.compile(r"\[([^]]+)]\(([^)]+)\)")


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kicked_users: list[int] = []

    async def on_ready(self):
        print(f"Logged in as {self.user} on {config.get_prod_string()}.")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return  # Don't bother with our own messages
        elif await is_admin(message.author):
            return  # Don't bother with messages from admins
        elif isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            return  # Don't bother in DMs

        # Actual message filtering
        content = message.content
        if await has_likely_scam(content):
            await message.delete()
            if message.author.id in self.kicked_users:
                try:
                    await message.author.ban(reason="Discord server invite ban")
                except discord.Forbidden:
                    print("Attempted to ban, but didn't have permission!")
                try:
                    await message.author.send(content=config.BAN_MESSAGE)
                except discord.Forbidden:
                    pass  # Didn't have permission to DM.
                try:
                    self.kicked_users.remove(message.author.id)
                except ValueError:
                    pass  # Double remove.
            else:
                try:
                    await message.author.kick(reason="Discord server invite kick")
                except discord.Forbidden:
                    print("Attempted to kick, but didn't have permission!")
                try:
                    await message.author.send(content=config.KICK_MESSAGE)
                except discord.Forbidden:
                    pass  # Didn't have permission to DM.
                self.kicked_users.append(message.author.id)


async def has_likely_scam(content: str) -> bool:
    if invite_regex.match(content):
        return True
    link_matches: list[tuple[str, str]] = link_regex.findall(content)
    if len(link_matches) > 0:
        for match in link_matches:
            text, link = match
            if "steam" in text:
                return True
    return False


async def is_admin(author: Union[discord.Member, discord.abc.User]):
    if (config.is_prod or not config.DEV_FILTER_ADMINS) and isinstance(author, discord.Member):
        return author.guild_permissions.administrator
    else:
        return False

if __name__ == "__main__":
    print("Run main.py!")
    sys.exit(1)
