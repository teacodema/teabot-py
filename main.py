from setup.keep_alive import keep_alive
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
import os
from discord.utils import get
from discord import FFmpegPCMAudio #, PCMVolumeTransformer
from youtube_dl import YoutubeDL
from discord.ext import commands, tasks
# import asyncio
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
from imports.system.server_data import *
from imports.system.msg_activity import *
from imports.system.msg_log import *
from imports.system.voice_activity import *
from imports.system.member_interaction import *
from imports.system.check_membership import *
from imports.system.role_reaction import *

from imports.member.audio_activity import *
from imports.member.fun_activity import *
# from imports.member.quran import *

intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)
# @client.command(pass_context=True)
# client2 = discord.Client(intents=intents)
bot = commands.Bot(intents = intents, command_prefix = 'tc_')
slash = SlashCommand(bot, sync_commands=True)
# bot = commands.Bot('!')

params = {
	'bot': bot,
	# 'client2': client2,
	'discord': discord,
	'slash': slash,
	'get': get,
	'tasks': tasks,
	'YoutubeDL': YoutubeDL,
	'FFmpegPCMAudio': FFmpegPCMAudio,
	'create_permission': create_permission,
	'SlashCommandPermissionType': SlashCommandPermissionType,
	# 'PCMVolumeTransformer': PCMVolumeTransformer,
	# 'asyncio': asyncio,
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
init_member_interaction(params)
init_check_membership(params)
init_role_reaction(params)
# init_quran(params)


keep_alive()
bot.run(os.getenv("token"))
