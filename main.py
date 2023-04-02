import discord
import os
from environs import Env
env = Env()
env.read_env()

client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(os.environ['TOKEN'])