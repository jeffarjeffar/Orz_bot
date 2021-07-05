import asyncio
import discord
from discord.ext import commands

import random
import textwrap
import io
import traceback
from contextlib import redirect_stdout

from Orz_bot.constants import *
from Orz_bot.util import util

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def time(self, ctx, time : float):
        await ctx.send(f'Setting timer for {time} seconds...')
        await asyncio.sleep(time)
        await ctx.send(f'{time} seconds is up!')
        
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')
    @commands.command()
    async def python(self, ctx, *, code):
        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        body = self.cleanup_code(code)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')
                
    @commands.command()
    async def cpp(self, ctx, *, code):
        code = self.cleanup_code(code)
        with open(os.path.join(TEMP_DIR, 'main.cpp'), 'w') as file:
            file.write(code)
        code, stdout, stderr = await util.run(f'g++ {os.path.join(TEMP_DIR, "main.cpp")} -o {os.path.join(TEMP_DIR, "a")}')
        # await ctx.send(f'{code}\n{stdout}\n{stderr}')
        # return
        if code != 0:
            await ctx.send(f'Compile error:\n```\n{stderr}```')
            return

        code, stdout, stderr = await util.time('./' + os.path.join(TEMP_DIR, "a"), 10)
        if code is None:
            await ctx.send('Time limit exceeded.')
        else:
            msg = None
            if code == 0:
                msg = f'```\n{stdout}```'
            else:
                msg = f'```\n{stdout}```\nRUNTIME ERROR\n```\n{stderr}```'
                
            try:
                await ctx.send(msg)
            except Exception as e:
                with open(os.path.join(TEMP_DIR, 'message.txt'), 'w') as file:
                    file.write(msg)
                await ctx.send(file=discord.File(os.path.join(TEMP_DIR, 'message.txt')))

def setup(bot):
    bot.add_cog(Misc(bot))
