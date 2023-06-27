import os
from datetime import datetime
from imports.data_server.config import *
from imports.actions.common import *
from imports.data_common.config import *
	
def start_loop(params):	
	bot = params['bot']
	tasks = params['tasks']
	@tasks.loop(hours=24, count=None, reconnect=False)
	async def am_alive():
		channel = bot.get_channel(textChannels['log-bot'])
		test_activated = ''
		if os.getenv("testing") == "1":
			test_activated = ' | **Test Mode Activated**'
		msg = f'From {os.getenv("platform")} - Ping @ {getTimeUtcPlusOne(datetime.now())}{test_activated}'
		await channel.send(msg.strip())
		await task_update_activity(params)
	am_alive.start()	

######################## BOT READY ########################
async def startBot(params):
	try:
		bot = params['bot']
		print("We have logged in as {0.user}".format(bot))
		await task_update_activity(params)
	except Exception as ex:
		print('----- startBot() -----')
		print(ex)
		await log_exception(ex, 'startBot()', None, bot)
