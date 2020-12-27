import discord
from discord.ext import commands
import asyncio

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
