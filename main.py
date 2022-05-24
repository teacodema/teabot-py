# from setup.keep_alive import keep_alive
import os
import disnake as discord
from disnake.ext import tasks, commands
from disnake import FFmpegPCMAudio #, PCMVolumeTransformer
from youtube_dl import YoutubeDL
# from setup.properties import *
# from setup.actions import *

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
bot = commands.Bot(intents = intents, command_prefix = 'tc_')

params = {
	'bot': bot,
	'discord': discord,
	'tasks': tasks,
	'commands': commands,
	'YoutubeDL': YoutubeDL,
	'FFmpegPCMAudio': FFmpegPCMAudio,
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
init_bot_reaction(params)
# init_quran(params)


# keep_alive()
bot.run(os.getenv("token"))
