import discord
import os
from discord.ext import commands

from cogs.orz import *
from cogs.Perms import *
from cogs.Utility import *
from cogs.Mute import *
from cogs.Misc import *
from cogs.Spam_detect import *

bot = commands.Bot(command_prefix = '!')

bot.add_cog(Orz(bot))
bot.add_cog(Perms(bot))
bot.add_cog(Mute(bot))
bot.add_cog(Misc(bot))
bot.add_cog(anti_spam(bot))

TOKEN = input('Token: ')

bot.run(TOKEN)

