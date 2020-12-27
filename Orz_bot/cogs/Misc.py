import discord
from discord.ext import commands
import asyncio
import random

from cogs.Utility import *

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spam(self, ctx, times, message):
        '''
        Sends <message> <times> number of times
        Make sure to surround <message> with quotes if it contains a space
        '''

        if getperm(ctx.message.author.id) < 69:
            await ctx.send('You do not have permission to spam')
            return

        for i in range(int(times)):
            await ctx.send(message)

    @commands.command()
    async def ding(self, ctx, user, points):
        '''
        Takes away participation points
        '''
        if not is_mooderator(ctx.message.author):
            await ctx.send('You do not have permission to ding people')
            return
            
        user_id = int(user[3:-1])

        if not user_id in penalty.keys():
            penalty[user_id] = 10
        penalty[user_id] += int(points)

        push_penalty()

        await ctx.send(f'Dang nang it <@{user_id}>\nThat\'s going to cost you {points} points')

    @commands.command()
    async def safety(self, ctx, user):
        if not is_mooderator(ctx.message.author):
            await ctx.send('You do not have permission to ding people')
            return
            
        user_id = int(user[3:-1])

        if not user_id in penalty.keys():
            penalty[user_id] = 10
        penalty[user_id] += 5

        push_penalty()

        messages = ['5 points for the chair!', 'Safety\n5 points']

        await ctx.send(random.choice(messages))