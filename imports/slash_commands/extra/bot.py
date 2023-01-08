
from imports.actions.common import *

def init_slash_commands_bot(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	states = ["online", "dnd", "idle", "offline"]
	discord_states = [ discord.Status.online, discord.Status.dnd, discord.Status.idle, discord.Status.offline]
	activity_types = ["watching", "listening", "playing"]
	discord_activity_types = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing]

	@bot.slash_command(name = "activity")
	async def tc_bot_activity(interaction, status=commands.Param(choices=states), activity_type=commands.Param(choices=activity_types), name = None):
		try:
			status = discord_states[states.index(status)]
			if name == None:
				name = "🌐 teacode.ma ☕"
			activity = discord.Activity(type = discord_activity_types[activity_types.index(activity_type)], name=name)
			await bot.change_presence(status=status, activity=activity)
		except Exception as ex:
			print('----- /tc_bot_activity() -----')
			print(ex)
			await log_exception(ex, '/tc_bot_activity', interaction)
