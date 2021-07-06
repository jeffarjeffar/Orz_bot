import discord
import discord_components as components

import sympy
import os

import constants

def to_png(tex, file):
	sympy.preview(tex, viewer='file', filename=file, euler=False)

curr_file = 0
async def send_tex(message):
	global curr_file

	filename = os.path.join(constants.TEMP_DIR, 'tex', str(curr_file) + '.png')
	curr_file += 1
	to_png(message.content, filename)
	await message.channel.send(file=discord.File(filename), components=[components.Button(label='Delete', id=curr_file)])
	return curr_file