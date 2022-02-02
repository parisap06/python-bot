import discord
from discord.ext import commands
import aiofiles

class Unwarn(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx, member: discord.Member=None, warning_index=None):
    # handle args
        if member is None:
           return await ctx.send("The provided member could not be found or you forgot to provide one.")

        if warning_index is None:
           return await ctx.send("You forgot to provide a warning index to remove.")

        if not warning_index.isdigit():
           return await ctx.send("The warning index is invalid.")
        
    # convert index str -> int
        warning_index = int(warning_index)
        warning_index -= 1 # make warning_index 0 based as !warnings starts at 1
 
    # try remove warning from dict
        try:
          self.client.warnings[ctx.guild.id][member.id][1].pop(warning_index)
          self.client.warnings[ctx.guild.id][member.id][0] -= 1

        except IndexError:
          return await ctx.send("Could not find a warning with that index.")

    # rewrite the file from updated dict (we must rewrite whole file)
        async with aiofiles.open(f"{ctx.guild.id}.txt", mode="w") as file: # "w" = clear and rewrite file
           for member_id in self.client.warnings[ctx.guild.id]: # loop through each warning in each member
               for admin_id, reason in self.client.warnings[ctx.guild.id][member_id][1]:
                   await file.write(f"{member.id} {ctx.author.id} {reason}\n")

        await ctx.send("Succesfully removed warning.")


def setup(client):
    client.add_cog(Unwarn(client))