import discord
from discord.ext import commands
import asyncio

from cogs.Mute_util import *
from cogs.Utility import *

class anti_spam(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.started = False

    @commands.command()
    async def spam_detect(self, ctx):
        if self.started == True:
            await ctx.send('Spam detection is already started')
            return
        self.started = True
        print('starting spam detection')
        await ctx.send('Starting spam detection')
        for k in message_counts.keys():
            message_counts[k] = 0
        general = self.client.get_channel(791145461829992508)
        while True:
            await asyncio.sleep(10)
            for k in message_counts.keys():
                #print(f'Found user {k} with {counts[k]} messages sent')
                if message_counts[k] >= 10:
                    await general.send(f'Dang nang it <@{k}>.\nOrz bot has detected that you have been spamming.\nI\'m going to have to ding you for that')
                    await mute(k, get_penalty(k), general.guild, general)
                message_counts[k] = 0
        spam_detected = False