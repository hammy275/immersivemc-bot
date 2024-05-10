import os
from typing import Union

# User Config

TEST_TOKEN: str = os.environ.get("IMMERSIVEMC_TOKEN_TEST")
PROD_TOKEN: str = os.environ.get("IMMERSIVEMC_TOKEN_PROD")

DEV_FILTER_ADMINS: bool = True  # Whether to filter admin messages in dev

KICK_MESSAGE: str = """You have been kicked from the ImmersiveMC Discord server.

You have very likely sent spam, or a Discord server invite link, which is not allowed by the server rules. You may send Discord server invites to users in DMs upon request, however they cannot be sent in the server itself.

Feel free to rejoin the ImmersiveMC Discord server if you want. No worries if you don't, though! If you have any questions, comments, or concerns, or you feel this happened in error, feel free to message <@195239733553659904>"""

BAN_MESSAGE: str = """You have been banned from the ImmersiveMC Discord server.

You have very likely sent spam, or a Discord server invite link, which is not allowed by the server rules. You may send them to users in DMs upon request, however they cannot be sent in the server itself.

If you would like to appeal this ban, message <@195239733553659904>."""

# End User Config
token: Union[str, None] = None  # Contains the token in use
is_prod: bool = False


def get_prod_string():
    return "production" if is_prod else "development"
