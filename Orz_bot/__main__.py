import discord
from discord.ext import commands

import os
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from Orz_bot.constants import *

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))


@bot.event
async def on_command_error(ctx, exc):
    if type(exc) == commands.errors.BotMissingPermissions:
        await ctx.send(f'Orz Bot is missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
    elif type(exc) == commands.errors.MissingRequiredArgument:
        await ctx.send(f'Missing required argument.\nPlease enter a value for: {exc.param}')
    elif (type(exc) == commands.errors.ArgumentParsingError or
          type(exc) == commands.errors.ExpectedClosingQuoteError or
          type(exc) == commands.errors.BadUnionArgument or
          type(exc) == commands.errors.UserInputError):
        await ctx.send(f'There was an error parsing your argument')
    elif type(exc) == commands.errors.TooManyArguments:
        await ctx.send(f'Bruh what why are there so many arguments?')
    elif type(exc) == commands.errors.CommandOnCooldown:
        await ctx.send(f'You are on cooldown. Try again in {round(exc.retry_after, 3)} seconds')
    elif type(exc) == commands.errors.CommandNotFound:
        await ctx.send('Command not found.')
    else:
        print('Command error found')

        # get data from exception
        etype = type(exc)
        trace = exc.__traceback__

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, exc, trace)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        print(traceback_text)

        await ctx.send('Uh oh. Something went wrong.')

        error_channel = bot.get_channel(LOGGING_CHANNEL)

        try:
            await error_channel.send(f'Command Error:\n```\n{traceback_text}\n```')
        except:
            with open(os.path.join(TEMP_DIR, 'message.txt'), 'w') as file:
                file.write(traceback_text)
            await error_channel.send(f'Command Error', discord.File(os.path.join(TEMP_DIR, 'message.txt')))


def setup():
    # Make required directories.
    for path in ALL_DIRS:
        os.makedirs(path, exist_ok=True)

    # logging to console and file on daily interval
    logging.basicConfig(format='{asctime}:{levelname}:{name}:{message}', style='{',
                        datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO,
                        handlers=[logging.StreamHandler(),
                                  TimedRotatingFileHandler(LOG_FILE_PATH, when='D',
                                                           backupCount=3, utc=True)])


def main():
    setup()
    
    cogs = [file.stem for file in Path('Orz_bot', 'cogs').glob('*.py')]
    for extension in cogs:
        bot.load_extension(f'Orz_bot.cogs.{extension}')
    logging.info(f'Cogs loaded: {", ".join(bot.cogs)}')
    
    token = input('Token? ')
    bot.run(token)


if __name__ == '__main__':
    main()