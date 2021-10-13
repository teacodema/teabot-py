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
from imports.bot_activity import *
from imports.role_activity import *
from imports.server_activity import *
from imports.server_data import *
from imports.msg_activity import *
from imports.msg_log import *
from imports.voice_activity import *
from imports.audio_activity import *
from imports.fun_activity import *
from imports.members_interaction import *
from imports.check_membership import *

intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)
# @client.command(pass_context=True)
# client2 = discord.Client(intents=intents)
client = commands.Bot(intents = intents, command_prefix = '$')
slash = SlashCommand(client, sync_commands=True)
# bot = commands.Bot('!')

params = {
    'client': client,
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
client.run(os.getenv("TOKEN"))
