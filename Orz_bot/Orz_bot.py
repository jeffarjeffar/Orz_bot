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
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='Tmw orz'))
    await send_to_gallery()


messages = []

@client.event
async def on_message(message):
    messages.append(message)

    #gallery = client.get_emoji(791402385436180500)
    #await message.add_reaction(gallery)
    #print('read message', message.content)

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
        command = message.content[1:].split(' ')
        if command[0] == 'ping':
            await message.channel.send('Pong!')
        if command[0] == 'mute':
            #print(message.author)
            if not is_admin(str(message.author)):
                await message.channel.send('You do not have permission to mute this user')
                return

            if len(command) != 3:
                await message.channel.send('Incorrect number of arguments given')
                return
            
            user_id = int(command[1][3:-1])
            #print(user_id)
            #print(message.guild)
            person = await message.guild.fetch_member(user_id)
            person_user = client.get_user(user_id) # person, but with type User
            #print(person)
            await mute(person, int(command[2]), message.guild, person_user.mention, message.channel)
        if command[0] == 'unmute':
            if not is_admin(str(message.author)):
                await message.channel.send('You do not have permission to mute this user')
                return
            if len(command) != 2:
                await message.channel.send('Incorrect number of arguments given')
                return

            user_id = int(command[1][3:-1])
            person = await message.guild.fetch_member(user_id)
            person_user = client.get_user(user_id) # person, but with type User
            await unmute(person, person_user.mention, message.channel)
        if command[0] == 'help':
            embed=discord.Embed(title="Help")
            embed.add_field(name="Commands", value='"mute [@user] [time]": mutes user for [time] seconds\n"Unmute [@user]": unmutes user', inline=False)
            embed.add_field(name="Help", value= '"help": Shows this message', inline=False)
            embed.add_field(name="Misc", value='"ping": Sends "Pong!"', inline=False)
            await message.channel.send(embed=embed)

async def mute(person, time, server, mention, channel):
    mute_msg = mention + ' has been muted for ' + str(time) + ' seconds'
    unmute_msg = mention + ' has been unmuted'
    error_msg = 'Unable to mute ' + mention
    for r in server.roles:
        #print('Found role', r.name)
        if r.name == 'Muted':
            if not r in person.roles:
                await person.add_roles(r)
                await channel.send(mute_msg)
                await asyncio.sleep(time)
            else:
                await channel.send(mention + ' is already muted')
                return
            if r in person.roles:
                await person.remove_roles(r)
                await channel.send(unmute_msg)
            return
    await channel.send(error_msg)

async def unmute(person, mention, channel):
    unmute_msg = mention + ' has been unmuted'
    for r in person.roles:
        if r.name == 'Muted':
            await person.remove_roles(r)
            await channel.send(unmute_msg)
            return
    await channel.send(mention + ' was not muted')

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
                embedVar = discord.Embed(title = str(msg.author), 
                   description = str(msg.content),
                   color = discord.Color.blue(),
                   url = msg.jump_url,
                   author = msg.author)
                
                await channel.send(embed=embedVar)
                await updated_message.clear_reaction(gallery)
        #print('Messages sent')
        messages.clear()
        await asyncio.sleep(120) # task runs every x seconds
client.run(' ')

