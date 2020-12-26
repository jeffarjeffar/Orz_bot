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

def is_mooderator(person):
    for role in person.roles:
        if role.name == 'Mooderator':
            return True
    return False

perms = {}

def pull_perms():
    F = open('perms.txt')
    f_perms = F.readlines()

    for p in f_perms:
        p2 = p.split('-----')
        perms[int(p2[0])] = int(p2[1])

def push_perms():
    F = open('perms.txt', 'w')
    for k in perms.keys():
        F.write(f'{k}-----{perms[k]}\n')

def getperm(id):
    if id in perms.keys():
        return perms[id]
    perms[id] = 0
    return 0

@client.event
async def on_ready():
    pull_perms()
    pull_penalty()
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='Tmw orz'))
    await spam_detect()
    await cow_worship()
    await send_to_gallery()


messages = []
counts = {}
penalty = {}
censored = []
censor_words = ['wtf']
replace = ['wtmoo']

def pull_penalty():
    F = open('penalty.txt')
    f_penalty = F.readlines()

    for p in f_penalty:
        p2 = p.split('-----')
        penalty[int(p2[0])] = int(p2[1])

def push_penalty():
    F = open('penalty.txt', 'w')
    for k in penalty.keys():
        F.write(f'{k}-----{penalty[k]}\n')

def get_penalty(user):
    if user in penalty.keys():
        penalty[user] = min(86400, penalty[user] * 2)
        return penalty[user]
    penalty[user] = 20
    push_penalty()
    return 10

@client.event
async def on_message(message):
    messages.append(message)
    if not message.author.bot:
        #print('updating counts')
        if not message.author.id in counts.keys():
            counts[message.author.id] = 0
        counts[message.author.id] = counts[message.author.id] + 1
        #print(f'count of user {message.author.id} is now
        #{counts[message.author.id]}')

    print(message.author.id, censored)
    if message.author.id in censored:
        censored_message = message.content
        for w in range(len(censor_words)):
            for i in range(len(censored_message) - len(censor_words[w]) + 1):
                print(i, censored_message[i:i+len(censor_words[w])])
                if censored_message[i:i + len(censor_words[w])] == censor_words[w]:
                    temp = censored_message[0:i]
                    temp += replace[w]
                    temp += censored_message[i + len(censor_words[w]):-1]
                    censored_message = temp
        if censored_message != message.content:
            await message.edit(content = censored_message)

    if str(message.channel) == 'welcome' and message.content == '':
        await welcome()

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
            if len(command) != 3:
                await message.channel.send('Incorrect number of arguments given')
                return
            
            user_id = int(command[1][3:-1])

            if getperm(user_id) >= getperm(message.author.id) and message.author.id != user_id:
                await message.channel.send('You do not have permission to mute this user')
                return

            await mute(user_id, int(command[2]), message.guild, message.channel)
        if command[0] == 'unmute':
            if not is_admin(str(message.author)):
                await message.channel.send('You do not have permission to unmute this user')
                return
            if len(command) != 2:
                await message.channel.send('Incorrect number of arguments given')
                return

            user_id = int(command[1][3:-1])

            await unmute(user_id, message.guild, message.channel)
        if command[0] == 'help':
            embed = discord.Embed(title="Help")
            embed.add_field(name="Commands", value='"mute [@user] [time]": mutes user for [time] seconds\n' + '"unmute [@user]": unmutes user\n' + '"setperms [@user] [permission]": Changes the permissions integer for a user\n' + '"viewperms": lists users and their permissions integers\n' + '"ding [@user] [points]": Takes away participation points from user\n' + '"censor [@user]": censors user\'s messages\n' + '"uncensor [@user]": uncensors user\'s messages', inline=False)
            embed.add_field(name="Help", value= '"help": Shows this message', inline=False)
            embed.add_field(name="Misc", value='"ping": Sends "Pong!"\n' + '"spam [times] [message]": sends message [time] number of times', inline=False)
            embed.add_field(name="Gallery", value='React with :gallery: to send a message to the gallery. It will be sent to the gallery if there are at least 2 reactions'
                            , inline=False)
            await message.channel.send(embed=embed)
        if command[0] == 'setperms':
            if not is_admin(str(message.author)):
                await message.channel.send('You do not have permission to change perms')
                return
            
            user_id = int(command[1][3:-1])
            perms[user_id] = int(command[2])
            push_perms()
            await message.channel.send('Permissions successfully updated')
        if command[0] == 'viewperms':
            res = ''
            for k in perms.keys():
                res += f'<@{k}>: {perms[k]}\n'
            await message.channel.send(res)
        if command[0] == 'spam':
            if getperm(message.author.id) < 69:
                await message.channel.send('You do not have permission to spam')
                return
            if len(command) <= 2:
                await message.channel.send('Incorrect number of arguments given')
                return

            msg = ''
            for i in range(2, len(command)):
                msg += command[i] + ' '
            for i in range(int(command[1])):
                await message.channel.send(msg)
        if command[0] == 'ding':
            if not is_mooderator(message.author):
                await message.channel.send('You do not have permission to ding people')
                return
            if len(command) != 3:
                await message.channel.send('Incorrect number of arguments given')
                return
            
            user_id = int(command[1][3:-1])

            penalty[user_id] += int(command[2])
            await message.channel.send(f'<@{user_id}> has been dinged')
        if command[0] == 'censor':
            if not is_mooderator(message.author):
                await message.channel.send('You do not have permission to censor people')
                return
            if len(command) != 2:
                await message.channel.send('Incorrect number of arguments given')
                return
            user_id = int(command[1][3:-1])
            if user_id in censored:
                await message.channel.send(f'<@{user_id}> is already censored')
            else:
                censored.append(user_id)
                await message.channel.send(f'<@{user_id}> has been censored')
        if command[0] == 'uncensor':
            if not is_mooderator(message.author):
                await message.channel.send('You do not have permission to uncensor people')
                return
            if len(command) != 2:
                await message.channel.send('Incorrect number of arguments given')
                return
            user_id = int(command[1][3:-1])
            if not user_id in censored:
                await message.channel.send(f'<@{user_id}> is not censored')
            else:
                censored.remove(user_id)
                await message.channel.send(f'<@{user_id}> has been uncensored')


async def mute(id, time, server, channel):
    person = await server.fetch_member(id)
    mute_msg = f'{person.mention} has been muted for {time} seconds'
    unmute_msg = f'{person.mention} has been unmuted'
    error_msg = f'Unable to mute {person.mention}'
    for r in server.roles:
        if r.name == 'Muted':
            if not r in person.roles:
                await person.add_roles(r)
                await channel.send(mute_msg)
                await asyncio.sleep(time)
            else:
                await channel.send(f'{person.mention} is already muted')
                return
            updated_person = await server.fetch_member(id)
            if r in updated_person.roles:
                await updated_person.remove_roles(r)
                await channel.send(unmute_msg)
            else:
                await channel.send(f'{time} seconds is up, but {person.mention} is already unmuted')
            return
    await channel.send(error_msg)

async def unmute(id, server, channel):
    person = await server.fetch_member(id)
    unmute_msg = f'{person.mention} has been unmuted'
    for r in person.roles:
        if r.name == 'Muted':
            await person.remove_roles(r)
            await channel.send(unmute_msg)
            return
    await channel.send(f'{person.mention} was not muted')

async def cow_worship():
    worship_channel = client.get_channel(791885828338352191)
    while True:
        await worship_channel.send(':pray: :cow:')
        await asyncio.sleep(696)

async def send_to_gallery():
    gallery = client.get_emoji(791402385436180500)

    channel = client.get_channel(791367434166468638)
    while True:
        for msg in messages:
            cnt = 0
            updated_message = await msg.channel.fetch_message(msg.id)
            for reaction in updated_message.reactions:
                if str(reaction.emoji) == '<:gallery:791402385436180500>':
                    cnt = reaction.count

            if cnt > 1:
                embedVar = discord.Embed(title = str(msg.author), 
                   description = str(msg.content),
                   color = discord.Color.blue(),
                   url = msg.jump_url,
                   author = msg.author)
                
                await channel.send(embed=embedVar)
                await updated_message.clear_reaction(gallery)
        messages.clear()
        await asyncio.sleep(120) # task runs every x seconds
async def spam_detect():
    general = client.get_channel(791145461829992508)
    while True:
        await asyncio.sleep(10)
        for k in counts.keys():
            #print(f'Found user {k} with {counts[k]} messages sent')
            if counts[k] >= 10:
                await general.send(f'Dang nang it <@{k}>.\nOrz bot has detected that you have been spamming.\nI\'m going to have to ding you for that')
                await mute(k, get_penalty(k), general.guild, general)
            counts[k] = 0

async def welcome():
    welcome_channel = client.get_channel(791124215561715714)

    await welcome_channel.send('Welcome to Lockout!\n:pray: :cow:')

client.run('')

