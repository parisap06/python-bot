import discord
from discord.ext import commands

class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
         if member is None:
             await ctx.send("Please mention someone to ban")
         if member.dm_channel == None:
              await member.create_dm()
              await member.dm_channel.send(
              content=f"You have been kicked from **{ctx.guild}** by **{ctx.message.author}**\nReason: **{reason}** ")
         await member.kick(reason=reason)
         await ctx.reply(f"**{member}** has been kicked :white_check_mark:\nReason: **{reason}** ")
         if member == ctx.message.author:
          await ctx.reply("You can't kick yourself :x:")

    @kick.error
    async def kick_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You can't do that :x:")
     if isinstance(error, commands.BadArgument):
        await ctx.reply("Member not found :confused:")

def setup(client):
    client.add_cog(Kick(client))   