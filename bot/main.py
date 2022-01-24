import os
import aiofiles
import asyncio
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix = ',', intents=intents)
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

#WARNING
@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member : discord.Member=None, *, reason=None):
        if member is None:
            await ctx.reply('Please mention someone to warn!')
        
        if reason is None:
            return await ctx.reply('Please provide a reason for the warning!')
        
        try:
            first_warning = False
            client.warnings[ctx.guild.id][member.id][0] += 1
            client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        except KeyError:
            first_warning = True
            client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        count = client.warnings[ctx.guild.id][member.id][0]

        async with aiofiles.open(f'{ctx.guild.id}.txt', mode='a') as file:
            await file.write(f'{member.id} {ctx.author.id} {reason}\n')
        
        await member.create_dm()
        await member.dm_channel.send(
        content=f'You have been warned from **{ctx.guild}** by **{ctx.message.author}**\nReason: **{reason}**\nTo check your warnings please use **,warnings** on the appropriate channel')
        await ctx.reply(f'{member.mention} has {count} {"warning" if first_warning else "warnings"}')

@client.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} Reason: **{reason}**.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")


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


client.run('INSERT TOKEN')
