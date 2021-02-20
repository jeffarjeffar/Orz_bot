import discord
from discord.ext import commands
import asyncio
import os

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

        if message.author == self.client.user:
            return

        if not message.author.id in message_counts.keys():
            message_counts[message.author.id] = 0
        message_counts[message.author.id] = message_counts[message.author.id] + 1

        if 'no u' in message.content.lower() and not is_admin(str(message.author)):
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

        if 'geniosity' in message.content.lower():
            geniosity = self.client.get_emoji(792822692231118918)
            await message.add_reaction(geniosity)
            
        if '69' in message.content.lower():
            geniosity = self.client.get_emoji(798664261534613554)
            await message.add_reaction(geniosity)
    
    @commands.Cog.listener()
    async def on_member_join(member):
        os.system('echo member_join')
        for channel in member.guild.channels:
            if channel.name.lower() == 'welcome':
                await channel.send(f'Welcome <@{member.id}>! Go to #handle-identify to identify your handle and access the rest of the server.\nNote: if you are a newbie, you can only send messages to #gitgud until you git gud\n:pray: :cow:')

