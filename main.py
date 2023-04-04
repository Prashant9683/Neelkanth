import discord
import os
from environs import Env
from discord.ext import commands
env = Env()
env.read_env()

client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send("Hello, I am online. You can use various commands to use me beginning with the prefix '!'.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!hello"):
        await message.channel.send("Namah Shivaya! I am your new helper...")
    if message.content.startswith("!help"):
        await message.channel.send("You can use the following commands to interact with me: \n"
                                   "!hello - I will greet you. \n"
                                   "!help - I will tell you what I can do for you. \n"
                                   "!about - I will tell you about myself. \n")
    if message.content.startswith("!about"):
        await message.channel.send("I am a Discord Bot. I am still learning. So, please be patient with me. I will be able to help you soon. Thank you for your patience!")
    if message.content.startswith("!test"):
        channel = client.get_channel(env.int('CHANNEL'))
        await channel.send("I am working fine. Thank you for testing me.")

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


client.run(os.environ['TOKEN'])