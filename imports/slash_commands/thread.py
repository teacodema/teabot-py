
from setup.actions.channel import *

def init_slash_commands_thread(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "tc_delete-threads")
	async def delete_threads(interaction, channel: discord.abc.GuildChannel, delete_archived=None):
		total_threads = channel.threads
		if delete_archived:
			total_threads = total_threads + await channel.archived_threads().flatten()
		for thread in total_threads:
			await thread.delete()
				