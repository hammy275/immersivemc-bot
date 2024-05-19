# ImmersiveMC Bot

Discord bot for ImmersiveMC's Discord server. Mainly provided so people can see the source code, though as long as you follow the LICENSE, feel free to do whatever you want with this! Do note that this is NOT built for general usage though, so it may not do exactly what you want.

## Setup

1. Set the environment variables `IMMERSIVEMC_TOKEN_TEST` and `IMMERSIVEMC_TOKEN_PROD` to the token(s) for your Discord bot(s). You can either use a separate bot for development/testing and for production, or use one for both.
2. Set the environment variables `IMMERSIVEMC_GUILD_IDS_TEST` and `IMMERSIVEMC_GUILD_IDS_PROD` to a comma-separated list of guild IDs for commands to be available in.
3. Invite to your Discord server.
4. ???
5. Profit!

## Features

- If someone sends a Discord invite, kick them and DM them about it. If they send another, ban them and DM them about it. Doesn't apply to admins in production, and tracking if a user has already been kicked is only done in memory, meaning bot restarts make the bot "forget" about any kicks.
