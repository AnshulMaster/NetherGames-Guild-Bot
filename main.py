from discord.ext import commands
from discord import Intents
from config import TOKEN
import os
import initialisation

client = commands.Bot(command_prefix="", intents=Intents.default())

async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

@client.event
async def on_ready():
    await load()
    try:
        sync = await client.tree.sync()
        print(sync)
        print("Synced all commands.")
    except Exception as e:
        print("Error in syncing commands:"+e)
    print("Bot is now online!")

initialisation.initialisation()
client.run(TOKEN)