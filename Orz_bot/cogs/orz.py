import discord
from discord.ext import commands
import discord_components as components

import random
import asyncio

from Orz_bot.constants import *
from Orz_bot.util import tex


class Orz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is ready. Logged in as {self.client.user}.')

    @commands.Cog.listener()
    async def on_message(self, message):
        powerful = ("mooderator" in [y.name.lower() for y in message.author.roles]
                    or "admin" in [y.name.lower() for y in message.author.roles]
                    or "orz bot" in [y.name.lower() for y in message.author.roles])

        if powerful and message.content.startswith('!ghost'):
            await message.delete()

        if not powerful and 'no u' in message.content.lower():
            await message.channel.send('No u.')

        if (not message.author.bot) and '$' in message.content:
            texed = await tex.send_tex(message)
            if texed is not None:
                await message.delete()

                def check(reaction, user):
                    return str(reaction.emoji) == '🗑️'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=696.9, check=check)
                except asyncio.TimeoutError:
                    await texed.clear_reactions()
                else:
                    await texed.delete()

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

    @commands.command()
    async def echo(self, ctx, *, msg):
        await ctx.send(msg)
        await ctx.message.delete()

    @commands.command(name='8ball')
    async def eightball(self, ctx, *, message):
        parsed = message.lower()
        e = discord.Embed(title=ctx.author.name + ' asked:', description=message,
                          color=0x9999ff)

        reponse = ''

        # rigged
        if 'fishy' in parsed and ('smart' in parsed or 'geniosity' in parsed):
            response = 'Fishy is geniosity.'
        elif 'apple method' in parsed and ('smart' in parsed or 'geniosity' in parsed):
            response = 'Apple Method is super geniosity.'
        elif 'larry' in parsed and ('smart' in parsed or 'geniosity' in parsed):
            response = f'Larry is super geniosity <:orz:{ORZ_ID}>'
        else:
            response = self.get_random_message()

        e.add_field(name='Answer:', value=response)
        await ctx.send(embed=e)

    def get_random_message(self):
        results = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]

        return random.choice(results)


def setup(bot):
    bot.add_cog(Orz(bot))
