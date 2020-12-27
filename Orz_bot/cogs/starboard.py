import discord
from discord.ext import commands
import asyncio

from cogs.Utility import *

class starboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def starboard(self, ctx):
        print('starting starboard')
        gallery = self.client.get_emoji(791402385436180500)

        channel = self.client.get_channel(791367434166468638)
        while True:
            for msg in messages:
                #print(f'Found message {msg.content}')
                cnt = 0
                updated_message = await msg.channel.fetch_message(msg.id)
                for reaction in updated_message.reactions:
                    if str(reaction.emoji) == '<:gallery:791402385436180500>':
                        cnt = reaction.count
                        break

                if cnt > 0:
                    embedVar = discord.Embed(title = str(msg.author), 
                       description = str(msg.content),
                       color = discord.Color.blue(),
                       url = msg.jump_url,
                       author = msg.author)
                
                    await channel.send(embed=embedVar)
                    await updated_message.clear_reaction(star)
            messages.clear()
            await asyncio.sleep(240) # task runs every x seconds