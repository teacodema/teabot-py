from setup.data.properties import *
from setup.actions.start import *
from setup.actions.common import *

def init_events_start(params):

	bot = params['bot']
	# discord = params['discord']
	# tasks = params['tasks']

	# states = ["online", "dnd", "idle", "offline"]
	# discord_states = [
	# 	discord.Status.online, discord.Status.dnd, discord.Status.idle
	# ]
	# types = ["watching", "listening", "playing"]
	# discord_types = [
	# 	discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing
	# ]

	######################## BOT READY ########################
	@bot.event
	async def on_ready():
		try:
			await startBot(params)
			start_loop(params)
		except Exception as ex:
			print('----- on_ready(evt) -----')
			print(ex)
			await log_exception(ex, 'on_ready(evt)', None, bot)
