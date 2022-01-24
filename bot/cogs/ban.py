import discord
from discord.ext import commands

class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
         if member.dm_channel == None:
             await member.create_dm()
             await member.dm_channel.send(
             content=f"You have been banned from **{ctx.guild}** by **{ctx.message.author}**\nReason: **{reason}** ")
         await member.ban(reason=reason)
         await ctx.reply(f"**{member.mention}** has been banned :white_check_mark:\nReason: **{reason}** ")
         if member == ctx.message.author:
               await ctx.reply("You can't ban yourself :x:")
               await client.process_commands(message)

    @ban.error
    async def ban_error(self, ctx, error):
         if isinstance(error, commands.MissingPermissions):
             await ctx.reply("You can't do that :x:")
         if isinstance(error, commands.BadArgument):
             await ctx.reply(f"This is not a valid member or member ID")
 
def setup(client):
    client.add_cog(Ban(client))   