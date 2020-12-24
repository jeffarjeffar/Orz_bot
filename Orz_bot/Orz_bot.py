import discord
from discord.ext import commands
import asyncio

prefix = ';'
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
    await client.change_presence(activity=discord.Game(name='Tmw orz'))


messages = []

@client.event
async def on_message(message):
    messages.append(message)

    #gallery = client.get_emoji(791402385436180500)
    #await message.add_reaction(gallery)

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
    #print('Watching for stars')

    gallery = client.get_emoji(791402385436180500)

    channel = client.get_channel(791367434166468638) # channel ID goes here
    while True:
        #print('Processing', len(messages), 'messages')
        for msg in messages:
            cnt = 0
            updated_message = await msg.channel.fetch_message(msg.id)
            #print('Found message', updated_message)
            for reaction in updated_message.reactions:
                #print('Found reaction', reaction, ', count = ',
                #reaction.count)
                #print(str(reaction.emoji))
                if str(reaction.emoji) == '<:gallery:791402385436180500>':
                    #print('Found stars')
                    cnt = reaction.count

            #print(cnt, 'people starred')
            if cnt > 0:
                #print(msg.author, msg.content)
                embedVar = discord.Embed(
                   title = str(msg.author), 
                   description = str(msg.content),
                   color = discord.Color.blue(),
                   url = msg.jump_url,
                   author = msg.author)
                
                await channel.send(embed=embedVar)
                await updated_message.clear_reaction(gallery)
        #print('Messages sent')
        messages.clear()
        await asyncio.sleep(30) # task runs every x seconds

client.run('insert super secret orz token here')

