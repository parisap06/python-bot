import discord
from discord.ext import commands
import aiofiles

class Warn(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member : discord.Member=None, *, reason=None):
        if member is None:
            await ctx.reply('Please mention someone to warn!')
        
        if reason is None:
            return await ctx.reply('Please provide a reason for the warning!')
        
        try:
            first_warning = False
            self.client.warnings[ctx.guild.id][member.id][0] += 1
            self.client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        except KeyError:
            first_warning = True
            self.client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        count = self.client.warnings[ctx.guild.id][member.id][0]

        async with aiofiles.open(f'{ctx.guild.id}.txt', mode='a') as file:
            await file.write(f'{member.id} {ctx.author.id} {reason}\n')
        
        await member.create_dm()
        await member.dm_channel.send(
        content=f'You have been warned from **{ctx.guild}** by **{ctx.message.author}**\nReason: **{reason}**\nTo check your warnings please use **,warnings** on the appropriate channel')
        await ctx.send(f'{member.mention} has {count} {"warning" if first_warning else "warnings"}')
   


def setup(client):
    client.add_cog(Warn(client))   