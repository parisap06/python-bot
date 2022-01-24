import discord
from discord.ext import commands

class Unban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
      banned_users = await ctx.guild.bans()
      member_name, member_discriminator = member.split ("#")

      for ban_entry in banned_users:
             user = ban_entry.user

             if (user.name, user.discriminator) == (member_name, member_discriminator):
              await ctx.guild.unban(user)
              await ctx.reply(f'{user.mention} has been unbanned :white_check_mark:')
              return
        


    @unban.error
    async def unban_error(ctx, error):
     if isinstance(error, commands.BadArgument):
        await ctx.reply(f'{user.mention} is not banned :smiley:')
     if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You can't do that :x:")

def setup(client):
    client.add_cog(Unban(client))   