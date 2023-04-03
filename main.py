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
    if message.content.startswith("!hello"):
        await message.channel.send("Namah Shivaya! I am your new helper...")
    if message.content.startswith("!help"):
        await message.channel.send("You can use the following commands to interact with me: \n"
                                   "$hello - I will greet you. \n"
                                   "$help - I will tell you what I can do for you. \n"
                                   "$about - I will tell you about myself. \n")
    if message.content.startswith("!about"):
        await message.channel.send("I am a Discord Bot. I am still learning. So, please be patient with me. I will be able to help you soon. Thank you for your patience!")

client.run(os.environ['TOKEN'])