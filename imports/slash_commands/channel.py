
from setup.actions.channel import *

def init_slash_commands_channel(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "hide-channel")
	async def tc_hide_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unhide:int = 0):
		"""
		Hide/Unhide channel for a role
		Parameters
		----------
		channel: target channel/category
		role: role to be affected by the change
		unhide: display the channel/category for the role
		"""
		try:
			await toggle_hide_channel(channel, role, bool(unhide))
		except Exception as ex:
			print('----- /hide_channel() -----')
			print(ex)
			await log_exception(ex, '/hide_channel', interaction)

	@bot.slash_command(name = "lock-channel")
	async def tc_lock_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unlock:int = 0):
		"""
		Lock/Unlock channel for a role
		Parameters
		----------
		channel: target channel
		role: role to be affected by the change
		unlock: unlock the channel/category for the role
		"""
		try:
			await toggle_lock_channel(channel, role, bool(unlock))
		except Exception as ex:
			print('----- /lock_channel() -----')
			print(ex)
			await log_exception(ex, '/lock_channel', interaction)

