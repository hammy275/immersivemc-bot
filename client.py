from typing import Union
import discord
from discord import app_commands
import sys
import re

import config
import tags

invite_regex: re.Pattern = re.compile(r"discord\.(gg/|com/invite)")
link_regex: re.Pattern = re.compile(r"\[([^]]+)]\(([^)]+)\)")


class Client(discord.Client):
    def __init__(self, do_sync: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_sync = do_sync
        self.kicked_users: list[int] = []
        self.tree = app_commands.CommandTree(self)
        self.allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True)
        # noinspection PyTypeChecker
        self.tree.add_command(discord.app_commands.Command(name="tag", description="Send premade text quickly.",
                callback=self.tag_command), guilds=config.PROD_GUILDS)

    async def sync_commands(self):
        print("Syncing commands to guilds.")
        guilds = config.PROD_GUILDS if config.is_prod else config.DEV_GUILDS
        for guild in guilds:
            await self.tree.sync(guild=guild)
        print("Commands synced!")

    async def tag_command(self, interaction: discord.Interaction, tag: str, user_to_ping: str = ""):
        is_error = False
        if not interaction.user.guild_permissions.administrator:
            response = "Only admins can use the /tag command."
            is_error = True
        else:
            tag = tag.lower()
            if tag in tags.TAGS:
                response = tags.TAGS[tag]
                if user_to_ping != "":
                    response = f"{user_to_ping}: {response}"
            else:
                response = "Tag not found."
                is_error = True
        await interaction.response.send_message(response, suppress_embeds=True, ephemeral=is_error)

    async def on_ready(self):
        print(f"Logged in as {self.user} on {config.get_prod_string()}.")
        if self.do_sync:
            await self.sync_commands()

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
