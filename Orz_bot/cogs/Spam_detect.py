import discord
from discord.ext import tasks
import asyncio

from cogs.Mute_util import *
from cogs.Utility import *

class anti_spam(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.spam_detect.start()

    @tasks.loop(seconds=10)
    async def spam_detect(self):
        general = self.client.get_channel(791145461829992508)
        for k in message_counts.keys():
            if message_counts[k] >= 13:
                await general.send(f'Dang nang it <@{k}>.\nOrz bot has detected that you have been spamming.\nI\'m going to have to ding you for that')
                await mute(k, get_penalty(k), general.guild, general)
            message_counts[k] = 0
            
    @spam_detect.before_loop
    async def wait_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()