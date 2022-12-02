
from setup.actions.channel import *

def init_slash_commands_thread(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "delete-threads")
	async def tc_delete_threads(interaction, channel: discord.abc.GuildChannel, delete_archived: int = 0):
		"""
		Delete Threads
		Parameters
		----------
		channel: target channel
		delete_archived: include archived threads - values 0/1
		"""
		try:
			total_threads = channel.threads
			if delete_archived:
				total_threads = total_threads + await channel.archived_threads().flatten()
			for thread in total_threads:
				await thread.delete()
		except Exception as ex:
			print('----- /delete_threads() -----')
			print(ex)
			await log_exception(ex, '/delete_threads', interaction)

