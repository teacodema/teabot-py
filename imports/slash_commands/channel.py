
from setup.actions.channel import *

def init_slash_commands_channel(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "hide-channel")
	async def hide_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role):
		"""
		Hide channel for a role
		Parameters
		----------
		channel: target channel
        role: role to be affected by the change
		"""
        try:
			await toggle_hide_channel(channel, role, False)
		except Exception as ex:
			print('----- /hide_channel() -----')
			print(ex)
			await log_exception(ex, '/hide_channel', interaction)

	@bot.slash_command(name = "show-channel")
	async def show_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role):
		"""
		Show channel for a role
		Parameters
		----------
		channel: target channel
        role: role to be affected by the change
		"""
        try:
			await toggle_hide_channel(channel, role, True)
		except Exception as ex:
			print('----- /show_channel() -----')
			print(ex)
			await log_exception(ex, '/show_channel', interaction)
	
	@bot.slash_command(name = "lock-channel")
	async def lock_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role):
		"""
		Lock channel for a role
		Parameters
		----------
		channel: target channel
        role: role to be affected by the change
		"""
        try:
			await toggle_lock_channel(channel, role, False)
		except Exception as ex:
			print('----- /lock_channel() -----')
			print(ex)
			await log_exception(ex, '/lock_channel', interaction)

	
	@bot.slash_command(name = "unlock-channel")
	async def unlock_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role):
		"""
		Unlock channel for a role
		Parameters
		----------
		channel: target channel
        role: role to be affected by the change
		"""
        try:
			await toggle_lock_channel(channel, role, True)
		except Exception as ex:
			print('----- /unlock_channel() -----')
			print(ex)
			await log_exception(ex, '/unlock_channel', interaction)
