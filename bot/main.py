import discord
import os
import aiofiles
import asyncio
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from itertools import cycle
import time
from datetime import datetime

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix = ',', intents=intents)
slash = SlashCommand(client)
status = cycle([',help', 'with Negotiator#0902'])
client.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}

#BOT UP
@client.event
async def on_ready():
    for guild in client.guilds:
        client.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
    change_status.start()
    print('Bot is ready.')

#WARN FETCH
@client.event
async def on_guild_join(guild):
    client.warnings[guild.id] = {}


#TASKS
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(next(status)))

#LOAD
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

#UNLOAD
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

#RELOAD
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('TOKEN')
