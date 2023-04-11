import discord
import os
from environs import Env
import pytz
import psycopg2
import pandas as pd
env = Env()
env.read_env()

client = discord.Client(intents=discord.Intents.all())

"""here this on ready event will be called when the bot is ready to use. It will print the name of the bot and the id 
of the bot and It will send a message to the channel that the bot is online."""
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send("Hello, I am online. You can use various commands to use me beginning with the prefix '!'.")
status_update = []

"""
here this on message event will be called when the bot will receive a message.
Now there are some commands that will be used to interact with the bot.
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    """
here the bot will send a message to the channel that the bot is online.
    """
    if message.content.startswith("!hello"):
        await message.channel.send("Namah Shivaya! I am your new helper...")
    if message.content.startswith("!help"):
        await message.channel.send("You can use the following commands to interact with me: \n"
                                   "!hello - I will greet you. \n"
                                   "!help - I will tell you what I can do for you. \n"
                                   "!about - I will tell you about myself. \n"
                                   "!record - I will record your status update. \n"
                                   "!status - I will show you the status updates of all the participants. \n"
                                   "!csv - I will send you the status updates in a csv file. \n")
    if message.content.startswith("!about"):
        await message.channel.send("I am a Discord Bot. I am still learning. So, please be patient with me. I will be "
                                   "able to help you soon. Thank you for your patience!")
    """
    This command will be used to record all the status updates of participants with name date and time.
    """
    if message.content.startswith("!record"):
        channel = client.get_channel(env.int('CHANNEL'))
        await message.channel.send("Type your message here, I am listening...")
        """
        The function check here returns the message which was sent by the user after the command !record.
        """
        def check(m):
            return m.author == message.author and m.channel == message.channel
        msg = await client.wait_for('message', check=check)
        status_update.append(msg.content + "\n - Sent by " + str(message.author) + " at " + str(message.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")) + " IST")
        await channel.send(msg.content) # This will send the message to the restricted channel (which will only be
        # accessible by mentors.

        """here this connects to the database and creates a table if it does not exist, stores all the status update 
        data to the table."""

        conn = psycopg2.connect(
            host='localhost',
            database=env.str('DATABASE'),
            user=env.str('USER'),
            password=env.str('PASSWORD'),
            port=env.str('PORT')
        )

        cursor = conn.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS status_update
                      (ID INT PRIMARY KEY     NOT NULL,
                      STATUS           TEXT    NOT NULL
                      ) '''
        cursor.execute(sql)
        abc = """SELECT ID FROM status_update"""
        cursor.execute(abc)
        row = cursor.rowcount
        data = [(0,), (1,), (0,)]
        if row >= 1:
            data = cursor.fetchall()
        existingIds = data[-1][0]
        print(existingIds)
        cursor.execute("INSERT INTO status_update (ID, STATUS) VALUES (%s, %s)",
                       (existingIds + 1, status_update[len(status_update) - 1]))
        print("List has been inserted to table successfully...")
        conn.commit()
        conn.close()
        await message.channel.send("Your message has been recorded successfully. Thank you for your update!")
    if message.content.startswith("!status"):
        channel = client.get_channel(env.int('CHANNEL')) # The variable CHANNEL here is the restricted channel which
        # will be accessible only by mentors. and the channel id should be written in the .env file.
        await channel.send("Here are the status updates: \n")
        conn = psycopg2.connect(
            host='localhost',
            database=env.str('DATABASE'),
            user=env.str('USER'),
            password=env.str('PASSWORD'),
            port=env.str('PORT')
        )

        cursor = conn.cursor()
        efg = """SELECT STATUS FROM status_update"""
        cursor.execute(efg)
        row = cursor.rowcount
        data = [(0,), (1,), (0,)]
        if row >= 1:
            data = cursor.fetchall()
        for i in data:
            await channel.send(i[0])
        conn.close()
    if message.content.startswith("!csv"):
        channel = client.get_channel(env.int('CHANNEL'))
        conn = psycopg2.connect(
            host='localhost',
            database=env.str('DATABASE'),
            user=env.str('USER'),
            password=env.str('PASSWORD'),
            port=env.str('PORT')
        )

        cursor = conn.cursor()
        df = pd.read_sql_query('SELECT * FROM status_update', conn)
        df.to_csv('table.csv', index=False)
        await channel.send(file=discord.File('table.csv'))
        conn.close()

"""
This event will be called when a new member joins the server.
"""
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has joined the server. Welcome to the server!')


"""
This event will be called when a member leaves the server.
"""
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
    channel = client.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has left the server. Goodbye!')

client.run(os.environ['TOKEN'])