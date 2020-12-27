import discord
from discord.ext import commands
import asyncio

from cogs.Utility import *

class Orz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pull_perms()
        pull_penalty()
        print('Bot is ready')

    @commands.command()
    async def ping(self, ctx):
        '''
        Sends "Pong!"
        '''
        await ctx.send('Pong!')
    
    @commands.command()
    async def orz(self, ctx):
        '''
        Sends ":orz:"
        '''
        orz = self.client.get_emoji(791359245454016523)
        await ctx.send(orz)

    @commands.Cog.listener()
    async def on_message(self, message):
        
        messages.append(message)

        if message.author.bot:
            return

        if not message.author.id in message_counts.keys():
            message_counts[message.author.id] = 0
        message_counts[message.author.id] = message_counts[message.author.id] + 1

        if 'no u' in message.content.lower():
            await message.channel.send('No u')

        if 'orz' in message.content.lower():
            orz = self.client.get_emoji(791359245454016523)
            await message.add_reaction(orz)

        if 'think' in message.content.lower() or 'thonk' in message.content.lower():
            thonk = self.client.get_emoji(791359264106610729)
            await message.add_reaction(thonk)

        if 'wtmoo' in message.content.lower():
            wtmoo = self.client.get_emoji(791368845172015104)
            await message.add_reaction(wtmoo)
        
