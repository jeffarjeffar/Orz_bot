import discord
from discord.ext import commands
import asyncio

from cogs.Utility import *

class Perms(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setperms(self, ctx, user, perm):
        '''
        Gives a permissions integer <perm> to <user>
        Users can only mute other users if they have higher permissions integers
        Users can only spam if they have 69 perms or more
        '''
        if not is_admin(str(ctx.message.author)):
            await ctx.send('You do not have permission to change perms')
            return
            
        user_id = int(user[3:-1])
        perms[user_id] = int(perm)
        push_perms()
        await ctx.send('Permissions successfully updated')

    @commands.command()
    async def viewperms(self, ctx):
        '''
        Lists the perms of each user (0 if not listed)
        '''
        if not is_mooderator(ctx.message.author):
            await ctx.send(f'Your permissions integer is {getperm(ctx.message.author.id)}')
            return

        res = ''
        for k in perms.keys():
            res += f'<@{k}>: {perms[k]}\n'
        await ctx.send(res)

    @commands.command()
    async def viewperm(self, ctx):
        '''
        Lists the perms of each user (0 if not listed)
        '''
        await ctx.send(f'Your permissions integer is {getperm(ctx.message.author.id)}')