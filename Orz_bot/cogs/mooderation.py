import discord
from discord.ext import commands
from discord.ext import tasks

import time

from Orz_bot.util import data


class Mooderation(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client
        self.mute_check.start()

    @commands.command()
    @commands.has_any_role('Mooderator', 'Admin', 'Moderator')
    async def mute(self, ctx, person: discord.Member, duration=''):
        if len(duration) > 0:
            if duration.endswith('h'):
                multiplier = 3600
            elif duration.endswith('m'):
                multiplier = 60
            elif duration.endswith('s'):
                multiplier = 1
            else:
                await ctx.send('Please specify a unit of time (h, m, or s)')
                return

            try:
                duration = float(duration[:-1]) * multiplier
                if duration <= 0:
                    await ctx.send('Please enter a positive real number')
                    
                endtime = time.time() + duration
                data.data_manager.change_mutetime(person.id, ctx.guild.id, endtime)
            except ValueError:
                await ctx.send(f'Bruh what please enter a real number')

        muted = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted in person.roles:
            await ctx.send(f'{person} is already muted!')
            return

        await person.add_roles(muted)
        await ctx.send(f'{person} has been muted')

    @commands.command()
    @commands.has_any_role('Mooderator', 'Admin', 'Moderator')
    async def unmute(self, ctx, person: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted in person.roles:
            await ctx.send(f'{person} is already unmuted!')
            return
        await person.remove_roles(muted)
        await ctx.send(f'{person} has been unmuted')

    @tasks.loop(seconds=1)
    async def mute_check(self):
        mutelist = data.data_manager.mutelist()
        for person in mutelist:
            if person[2] <= time.time():
                guild = await self.client.fetch_guild(person[1])
                member = await guild.fetch_member(person[0])
                muted = discord.utils.get(guild.roles, name="Muted")
                await member.remove_roles(muted)
                data.data_manager.remove_mutetime(person[0], person[1])

    @mute_check.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready...')
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Mooderation(bot))
