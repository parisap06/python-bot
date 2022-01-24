import discord
from discord.ext import commands

class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
     await ctx.message.delete()
     await ctx.channel.purge(limit=amount)
     await ctx.send(f'**{amount} messages have been deleted. <@{ctx.author.id}>**', delete_after=2)
     await client.process_commands(message)
    
    @purge.error
    async def clean_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions): 
        await ctx.reply("You can't do that :x:")

def setup(client):
    client.add_cog(Purge(client))        