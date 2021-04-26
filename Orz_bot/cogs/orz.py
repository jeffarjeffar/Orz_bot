import discord
from discord.ext import commands

from Orz_bot.constants import *


class Orz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        powerful = ("mooderator" in [y.name.lower() for y in message.author.roles]
                    or "admin" in [y.name.lower() for y in message.author.roles]
                    or "orz bot" in [y.name.lower() for y in message.author.roles])

        if not powerful and 'no u' in message.content.lower():
            await message.ctx.send('No u.')

        if 'orz' in message.content.lower():
            orz = self.client.get_emoji(ORZ_ID)
            await message.add_reaction(orz)

        if 'think' in message.content.lower() or 'thonk' in message.content.lower():
            thonk = self.client.get_emoji(THONK_ID)
            await message.add_reaction(thonk)

        if 'wtmoo' in message.content.lower():
            wtmoo = self.client.get_emoji(WTMOO_ID)
            await message.add_reaction(wtmoo)

        if 'geniosity' in message.content.lower():
            geniosity = self.client.get_emoji(GENIOSITY_ID)
            await message.add_reaction(geniosity)

        if '69' in message.content.lower():
            geniosity = self.client.get_emoji(NOICE_ID)
            await message.add_reaction(geniosity)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency is {round(1000 * self.client.latency, 2)}ms')

    @commands.command()
    @commands.has_any_role('Mooderator', 'Admin', 'Moderator')
    async def spam(self, ctx, times: int, *, msg):
        for _ in range(times):
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Orz(bot))
