import discord
from discord.ext import commands
import asyncio

from cogs.Utility import *

class starboard(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.started = False

    @commands.command()
    async def reset(self, ctx):
        if not is_mooderator(ctx.author):
            await ctx.send('You do not have permission to reset starboard')
            return
        messages.clear()
        await ctx.send('Starboard has been reset')

    @commands.command()
    async def starboard(self, ctx):
        if self.started == True:
            await ctx.send('Starboard is already started')
            return
        self.started = True
        print('starting starboard')
        await ctx.send('Starting starboard')

        gallery = self.client.get_emoji(791402385436180500)

        channel = self.client.get_channel(791367434166468638)

        while True:
            #print(f'Found {len(messages)} messages')
            for msg in messages:
                cnt = 0
                updated_message = await msg.channel.fetch_message(msg.id)
                for reaction in updated_message.reactions:
                    if str(reaction.emoji) == '<:gallery:791402385436180500>':
                        cnt = reaction.count
                        print(f'Found message {msg.content} with {cnt} stars')
                        break

                if cnt > 1:
                    embedVar = discord.Embed(title = str(msg.author), 
                       description = str(msg.content),
                       color = discord.Color.blue(),
                       url = msg.jump_url,
                       author = msg.author)
                
                    await channel.send(embed=embedVar)
                    messages.remove(msg)
            await asyncio.sleep(5) # task runs every x seconds
        star_started = False