from imports.data.properties import *
from imports.actions.start import *
from imports.actions.common import *

def init_events_start(params):

	bot = params['bot']

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
