import discord
from discord.ext import commands
import asyncio

from cogs.Utility import *
from cogs.Mute_util import *

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mute(self, ctx, user, time):
        '''
        mutes a user for <time> seconds
        '''
        user_id = int(user[3:-1])

        if getperm(user_id) >= getperm(ctx.message.author.id) and ctx.message.author.id != user_id:
            await ctx.send('You do not have permission to mute this user')
            return

        await mute(user_id, int(time), ctx.message.guild,ctx. message.channel)

    @commands.command()
    async def unmute(self, ctx, user):
        '''
        unmutes a user
        '''
        if not is_mooderator(ctx.message.author):
            await ctx.send('You do not have permission to unmute this user')
            return

        user_id = int(user[3:-1])
        await unmute(user_id, ctx.message.guild, ctx.message.channel)
