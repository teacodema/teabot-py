import os
from datetime import datetime
from setup.data.properties import *
from setup.actions.common import *
	
def start_loop(params):	
	bot = params['bot']
	tasks = params['tasks']
	@tasks.loop(hours=3, count=None, reconnect=False)
	async def am_alive():
		channel = bot.get_channel(textChannels['log-bot'])
		msg = f'From {os.getenv("platform")} - Ping at {getTimeUtcPlusOne(datetime.now())}'
		await channel.send(msg)
	am_alive.start()	

######################## BOT READY ########################
async def startBot(params):
	try:
		bot = params['bot']
		discord = params['discord']
		print("We have logged in as {0.user}".format(bot))
		status = discord.Status.online
		activity = discord.Activity(type=discord.ActivityType.watching, name="🌐 teacode.ma ☕")
		await bot.change_presence(status=status, activity=activity)
		# # activity = discord.Activity(type=discord.ActivityType.watching, name="teacode.ma")
		# # activity = discord.Game(name="https://teacode.ma", type=3)
		# # class discord.CustomActivity(name, *, emoji=None, **extra)
		task_update_activity(params)
	except Exception as ex:
		print('----- startBot() -----')
		print(ex)
		await log_exception(ex, 'startBot()', None, bot)
