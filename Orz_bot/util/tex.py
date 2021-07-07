import discord

import pnglatex
import os

from Orz_bot import constants


def to_png(tex, file):
    pnglatex.pnglatex(tex, file)


curr_file = 0


async def send_tex(message):
    global curr_file

    os.makedirs(os.path.join(constants.TEMP_DIR, 'tex'), exist_ok=True)
    filename = os.path.join(constants.TEMP_DIR, 'tex', str(curr_file) + '.png')
    curr_file += 1
    try:
        to_png(message.content, filename)
    except ValueError:
        return None
    embed = discord.Embed(
        title=f'{message.author}', description=message.content)
    file = discord.File(filename, filename='tex.png')
    embed.set_image(url='attachment://tex.png')
    msg = await message.channel.send(embed=embed, file=file)
    await msg.add_reaction('🗑️')
    return msg
