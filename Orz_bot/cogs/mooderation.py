import discord
from discord.ext import commands

import time


class Mooderation(commands.Cog):

	def __init__(self, client) -> None:
		self.client = client

	@commands.command()
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
			except ValueError:
				await ctx.send(f'Bruh what please enter a real number')
		else:
			await person.edit(mute=True)
