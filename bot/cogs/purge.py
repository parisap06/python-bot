import discord
from discord.ext import commands
import asyncio

class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int):
     if amount > 2000:
         await ctx.send(embed=discord.Embed(description="You can't delete more than 2000 messages!",
         color=discord.Colour.red()))
     
     else:
       count_members = {}
       messages = await ctx.channel.history(limit=amount).flatten()
       for message in messages[1:]:
          if str(message.author) in count_members:
              count_members[str(message.author)] += 1
          else:
              count_members[str(message.author)] = 1
       new_string = []
       deleted_messages = 0
       for author, message_deleted in list(count_members.items()):
           new_string.append(f'**{author}**: {message_deleted}')
           deleted_messages += message_deleted
       final_string = '\n'.join(new_string)
       await ctx.channel.purge(limit=amount+1)
       if deleted_messages == 1:
           msg = await ctx.send(f'{deleted_messages} message was removed.\n\n{final_string}')
       elif deleted_messages == 0:
           msg = await ctx.send("No messages were deleted. Make sure the messages aren't older than 2 weeks")
       else:
           msg = await ctx.send(f'{deleted_messages} messages were removed.\n\n{final_string}')

       await asyncio.sleep(3)
       await msg.delete()
    
    @purge.error
    async def clean_error(self, ctx, error):
     if isinstance(error, commands.MissingPermissions): 
        await ctx.reply("You can't do that :x:")

def setup(client):
    client.add_cog(Purge(client))        