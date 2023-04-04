import discord
import os
from environs import Env
from datetime import datetime
import pytz
from discord.ext import commands
env = Env()
env.read_env()

client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send("Hello, I am online. You can use various commands to use me beginning with the prefix '!'.")
status_update = []
@client.event
async def on_message(message):
    specific_channel = client.get_channel(env.int('CHANNEL'))
    general_channel = client.get_channel(env.int('GENERAL_CHANNEL'))
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
    if message.content.startswith("!record"):
        channel = client.get_channel(env.int('CHANNEL'))
        await message.channel.send("Type your message here, I am listening...")
        def check(m):
            return m.author == message.author and m.channel == message.channel
        msg = await client.wait_for('message', check=check)
        status_update.append(msg.content + "\n - Sent by " + str(message.author) + " at " + str(message.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")) + " IST")
        await channel.send(msg.content)
    if message.content.startswith("!status"):
        channel = client.get_channel(env.int('CHANNEL'))
        await channel.send("Here are the status updates: \n")
        for i in status_update:
            await channel.send(i)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has left the server.')


@client.event
async def copy(ctx, message):
    await ctx.send(message)

client.run(os.environ['TOKEN'])