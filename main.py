from setup.keep_alive import keep_alive
import discord
from discord_slash import SlashCommand
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands, tasks
# import time
# import datetime
# from threading import Timer
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from setup.properties import *
from setup.actions import *

from imports.system.bot_activity import *
from imports.system.role_activity import *
from imports.system.server_activity import *
from imports.system.msg_activity import *
from imports.system.msg_log import *
from imports.system.voice_activity import *
from imports.system.members_interaction import *
from imports.system.check_membership import *

from imports.common.server_data import *

from imports.member.audio_activity import *
from imports.member.fun_activity import *

intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)
# @client.command(pass_context=True)
# client2 = discord.Client(intents=intents)
bot = commands.Bot(intents = intents, command_prefix = '$')
slash = SlashCommand(bot, sync_commands=True)
# bot = commands.Bot('!')

params = {
    'bot': bot,
		# 'client2': client2,
    'discord': discord,
    'slash': slash,
    'get': get,
		'tasks': tasks,
    # 'bot': bot,
    'YoutubeDL': YoutubeDL,
    'FFmpegPCMAudio': FFmpegPCMAudio
}

init_bot_activity(params)
init_role_activity(params)
init_server_activity(params)
init_server_data(params)
init_msg_activity(params)
init_msg_log(params)
init_voice_activity(params)
init_audio_activity(params)
init_fun_activity(params)
init_members_interaction(params)
init_check_membership(params)


keep_alive()
bot.run(os.getenv("TOKEN"))
