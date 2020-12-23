import discord
from discord.ext import commands
import asyncio

prefix = '='
version = '1.0.0'

client = discord.Client()

def is_admin(person):
    F = open('admin.txt')
    admins = F.readlines()

    for i in range(len(admins)):
        if (admins[i] == person):
            return True
    return False
    

@client.event
async def on_ready():
    await send_to_gallery()
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='TMW ORZ'))


messages = []

@client.event
async def on_message(message):
    messages.append(message)

    gallery = client.get_emoji(791402385436180500)
    await message.add_reaction(gallery)

    if message.author == client.user:
        return

    if 'no u' in message.content.lower():
        await message.channel.send('No u')

    if 'orz' in message.content.lower():
        orz = client.get_emoji(791359245454016523)
        await message.add_reaction(orz)

    if 'think' in message.content.lower() or 'thonk' in message.content.lower():
        thonk = client.get_emoji(791359264106610729)
        await message.add_reaction(thonk)

    if 'wtmoo' in message.content.lower():
        wtmoo = client.get_emoji(791368845172015104)
        await message.add_reaction(wtmoo)

    if message.content.startswith(prefix):
        # commands
        if message.content.startswith(prefix + 'ping'):
            await message.channel.send('Pong!')

async def send_to_gallery():
    print('Watching for stars')

    gallery = client.get_emoji(791402385436180500)

    channel = client.get_channel(791367434166468638) # channel ID goes here
    while True:
        print('Processing', len(messages), 'messages')
        for msg in messages:
            cnt = 0
            for reaction in msg.reactions:
                if reaction == gallery:
                    cnt += 1

            if cnt > 1:
                channel.send(msg)
        print('Messages sent')
        messages.clear()
        await asyncio.sleep(60) # task runs every 60 seconds

client.run('NzkxMzQwNzMwOTA3ODg1NjA4.X-NvfA.rsLYWSO4K752BD0nv2T6se-eP0A')

