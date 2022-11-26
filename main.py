# from setup.keep_alive import keep_alive
import os
import disnake as discord
from disnake.ext import tasks, commands
from disnake import FFmpegPCMAudio #, PCMVolumeTransformer
from youtube_dl import YoutubeDL
# from setup.properties import *
# from setup.actions import *
from imports.events.start import *
from imports.events.message import *
from imports.events.reaction import *
from imports.events.voice import *
from imports.events.member import *
from imports.events.slash_commands import *
from imports.events.scheduled_event import *

from imports.slash_commands.info import *
from imports.slash_commands.message import *
from imports.slash_commands.reaction import *
from imports.slash_commands.voice import *
# from imports.slash_commands.audio import *
from imports.slash_commands.member import *
from imports.slash_commands.role import *
from imports.slash_commands.scheduled_event import *
from imports.slash_commands.extra.fun import *
# from imports.member.quran import *

intents = discord.Intents.all()
bot = commands.Bot(intents = intents)

params = {
	'bot': bot,
	'discord': discord,
	'tasks': tasks,
	'commands': commands,
	'YoutubeDL': YoutubeDL,
	'FFmpegPCMAudio': FFmpegPCMAudio,
}

def init_events():
	init_events_start(params)
	init_events_message(params)
	init_events_reaction(params)
	init_events_voice(params)
	init_events_member(params)
	init_events_slash_commands(params)
	init_events_scheduled_event(params)
# init_quran(params)

def init_slash_commands():
	init_slash_commands_info(params)
	init_slash_commands_message(params)
	init_slash_commands_reaction(params)
	init_slash_commands_voice(params)
	# init_slash_commands_audio(params)
	init_slash_commands_member(params)
	init_slash_commands_role(params)
	init_slash_commands_scheduled_event(params)
	init_slash_commands_extra(params)


init_events()
init_slash_commands()


# keep_alive()
bot.run(os.getenv("token"))
