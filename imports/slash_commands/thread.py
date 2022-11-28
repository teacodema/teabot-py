
from setup.actions.channel import *

def init_slash_commands_thread(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "tc_delete-threads")
	async def delete_threads(interaction, channel: discord.abc.GuildChannel, delete_archived=None):
		for thread in channel.threads:
			if not thread.archived:
				await thread.delete()
        if delete_archived:
			archived_threads = await channel.archived_threads().flatten()
			for thread in archived_threads:
				await thread.delete()
				