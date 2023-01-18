
from imports.actions.channel import *

def init_slash_commands_thread(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "thread-archive")
	async def tc_thread_archive(interaction, channel: discord.abc.GuildChannel):
		"""
		Archive Threads
		Parameters
		----------
		channel: target channel
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			for thread in channel.threads:
				await thread.edit(archived=True)
		except Exception as ex:
			print('----- /tc_thread_archive() -----')
			print(ex)
			await log_exception(ex, '/tc_thread_archive', interaction)


	@bot.slash_command(name = "thread-delete")
	async def tc_thread_delete(interaction, channel: discord.abc.GuildChannel, delete_archived: int = 0):
		"""
		Delete Threads
		Parameters
		----------
		channel: target channel
		delete_archived: include archived threads - values 0/1 - default 0
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			total_threads = channel.threads
			if delete_archived:
				total_threads = total_threads + await channel.archived_threads().flatten()
			for thread in total_threads:
				await thread.delete()
		except Exception as ex:
			print('----- /tc_thread_delete() -----')
			print(ex)
			await log_exception(ex, '/tc_thread_delete', interaction)

