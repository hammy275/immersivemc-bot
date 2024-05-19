import discord
import sys

import client
import config

if __name__ == "__main__":
    # Uses production token if "prod" in the second argument or if we're running from pythonw
    # Uses dev token if "dev" or "test" in the second argument or if we're not running from pythonw.
    has_arg = len(sys.argv) >= 2
    do_sync = "sync" in sys.argv

    if has_arg and "prod" in sys.argv[1].lower():
        config.token = config.PROD_TOKEN
        config.is_prod = True
    elif has_arg and ("dev" in sys.argv[1].lower() or "test" in sys.argv[1].lower()):
        config.token = config.TEST_TOKEN
        config.is_prod = False
    elif has_arg and not do_sync:
        print("Invalid extra argument! Expected 'sync', 'dev', 'test', or 'prod'.")
        sys.exit(1)
    elif "pythonw" in sys.executable:
        config.token = config.PROD_TOKEN
        config.is_prod = True
    else:
        config.token = config.TEST_TOKEN
        config.is_prod = False

    # Don't need to store both tokens anymore
    config.TEST_TOKEN = ""
    config.PROD_TOKEN = ""

    print(f"Running in {config.get_prod_string()}")
    intents = discord.Intents.default()
    intents.message_content = True

    client = client.Client(do_sync=do_sync, intents=intents)
    client.run(config.token)
