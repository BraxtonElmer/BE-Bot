import discord
import os
from discord.ext import commands
import mysql.connector
from pretty_help import PrettyHelp
import config
import asyncio

print("Starting bot")

prefixes = ['Be ','bE ','BE ','be ']
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefixes, help_command=PrettyHelp(), intents = intents)

print("Importing cogs")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

print("cogs imported")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('be help'))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hi! I am BE Bot, pronounced as BeYee Bot. I was created by Braxton Elmer.')
            await asyncio.sleep(2)
            client.change_presence(activity=discord.Game('be help'))
        break

@client.event
async def on_guild_remove(guild):
    mydb = mysql.connector.connect(
    host=config.sql_host,
    user=config.sql_user,
    password=config.sql_pass,
    database=config.sql_db
    )
    mycursor = mydb.cursor()
    delete_guild_sql = "DELETE FROM `server_data` WHERE `server_id`='"+str(guild.id)+"'"
    mycursor.execute(delete_guild_sql)
    mydb.commit()






client.run(config.key)
