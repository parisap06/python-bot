import discord
from discord.ext import commands
import aiofiles

class Warnings(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.Member=None):
     if member is None:
        return await ctx.reply("The provided member could not be found or you forgot to provide one.")
     pfp = member.avatar_url
     embed = discord.Embed(title=f"Displaying warnings for {member}", description="", colour=discord.Colour.red())
     embed.set_footer(icon_url= f"{member.avatar_url}")
     try:
        i = 1
        for admin_id, reason in self.client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} Reason: **{reason}**.\n"
            i += 1

        await ctx.send(embed=embed)

     except KeyError: # no warnings
        await ctx.send("This user has no warnings.")
   


def setup(client):
    client.add_cog(Warnings(client))   