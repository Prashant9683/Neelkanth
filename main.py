import discord
from environs import Env
import pytz
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, URL
from discord import app_commands
from discord.ext import commands
env = Env()
env.read_env()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
status_update = []
status_general = []
time = []
user = []

"""here this on ready event will be called when the bot is ready to use. It will print the name of the bot and the id 
of the bot and It will send a message to the channel that the bot is online."""

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    channel = bot.get_channel(env.int('GENERAL_CHANNEL'))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        await channel.send("Hello, I am online. You can use various commands to use me beginning with the prefix '/'.")
    except Exception as e:
        print(e)


"""
This event will be called when a new member joins the server.
"""

@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    channel = bot.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has joined the server. Welcome to the server!')

"""
This event will be called when a member leaves the server.
"""

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
    channel = bot.get_channel(env.int('GENERAL_CHANNEL'))
    await channel.send(f'{member} has left the server. Goodbye!')

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Namah Shivaya! {interaction.user.mention} I am your new helper...",
                                            ephemeral=True)

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"You can use the following commands to interact with me: \n"
                                            "/hello - I will greet you. \n"
                                            "/help - I will tell you what I can do for you. \n"
                                            "/about - I will tell you about myself. \n"
                                            "/record - I will record your status update. \n"
                                            "/status - I will show you the status updates of all the participants. \n"
                                            "/csv - I will send you the status updates in a csv file. \n",
                                            ephemeral=True)
@bot.tree.command(name="about")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am a bot created by the lovely people of C cube. I am here to help "
                                            f"you with your daily status updates. You can use the following commands "
                                            f"to interact with me: \n"
                                            "/hello - I will greet you. \n"
                                            "/help - I will tell you what I can do for you. \n"
                                            "/about - I will tell you about myself. \n"
                                            "/record - I will record your status update. \n"
                                            "/status - I will show you the status updates of all the participants. \n"
                                            "/csv - I will send you the status updates in a csv file. \n",
                                            ephemeral=True)

    """
    This command will be used to record all the status updates of participants with name date and time.
    """


@bot.tree.command(name="record")
@app_commands.describe(thing_to_say = "Type your message here, I am listening...")
async def record(interaction: discord.Interaction, thing_to_say: str):
    channel = bot.get_channel(env.int('CHANNEL'))  # The variable CHANNEL here is the restricted channel which
        # will be accessible only by mentors. and the channel id should be written in the .env file.
    status_general.append(thing_to_say + "\n - Sent by " + str(interaction.user) + " at " + str(interaction.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")) + " IST")
    status_update.append(thing_to_say)
    time.append(str(interaction.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")) + " IST")
    user.append(str(interaction.user))
    await channel.send(thing_to_say)

    """here this connects to the database and creates a table if it does not exist, stores all the status update 
    data to the table."""

    conn = psycopg2.connect(
        host=env.str('HOST'),
        database=env.str('DATABASE'),
        user=env.str('USER'),
        password=env.str('PASSWORD'),
        port=env.str('PORT')
    )
    cursor = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS status_update
    (ID INT PRIMARY KEY     NOT NULL,
    STATUS           TEXT    NOT NULL,
    USERN            TEXT    NOT NULL,
    TIME            TEXT    NOT NULL,
    DATE            TEXT    NOT NULL
    )'''
    sql2 = '''CREATE TABLE IF NOT EXISTS status_update2
                            (ID INT PRIMARY KEY     NOT NULL,
                            STATUS_GENERAL           TEXT    NOT NULL
                            ) '''
    cursor.execute(sql)
    cursor.execute(sql2)
    abc = """SELECT ID FROM status_update"""
    cursor.execute(abc)
    row = cursor.rowcount
    data = [(0,), (1,), (0,)]
    if row >= 1:
        data = cursor.fetchall()
    existingIds = data[-1][0]
    cursor.execute("INSERT INTO status_update (ID, STATUS, USERN, TIME) VALUES (%s, %s, %s, %s)",
                   (existingIds + 1, status_update[len(status_update) - 1], user[len(user) - 1], time[len(time) - 1]))
    cursor.execute("INSERT INTO status_update2 (ID, STATUS_GENERAL) VALUES (%s, %s)",
                   (existingIds + 1, status_general[len(status_general) - 1]))
    print("List has been inserted to table successfully...")
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"Your message has been recorded. Thank you for your update!",
                                            ephemeral=True)

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(f"Check all the status updates in the respective channel", ephemeral=True)
    channel = bot.get_channel(env.int('CHANNEL'))
    await channel.send("Here are the status updates: \n")
    conn = psycopg2.connect(
        host='localhost',
        database=env.str('DATABASE'),
        user=env.str('USER'),
        password=env.str('PASSWORD'),
        port=env.str('PORT')
    )

    cursor = conn.cursor()
    efg = """SELECT STATUS_GENERAL FROM status_update2"""
    cursor.execute(efg)
    row = cursor.rowcount
    data = [(0,), (1,), (0,)]
    if row >= 1:
        data = cursor.fetchall()
    for i in data:
        await channel.send(i[0])
    conn.close()

@bot.tree.command(name="csv")
async def csv(interaction: discord.Interaction):
    await interaction.response.send_message(f"Check your csv file in the respective channel", ephemeral=True)
    channel = bot.get_channel(env.int('CHANNEL'))
    url_object = URL.create(
        "postgresql",
        username=env.str('USER'),
        password=env.str('PASSWORD'),
        host="localhost",
        database=env.str('DATABASE'),
        port=env.str('PORT')
    )
    engine = create_engine(url_object)
    df = pd.read_sql_query('SELECT * FROM status_update', engine)
    df.to_csv('table.csv', index=False)
    await channel.send(file=discord.File('table.csv'))
    engine.dispose()

bot.run(env.str('TOKEN'))