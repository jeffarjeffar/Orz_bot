import discord
from discord.ext import commands


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

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency is {round(1000 * self.client.latency, 2)}ms')


def setup(bot):
    bot.add_cog(Orz(bot))
