
from imports.actions.channel import *
from imports.actions.common import *
from imports.data_server.config import *
from imports.data_server.channels_categories import *

def init_slash_commands_channel(params):
	
	bot = params['bot']
	discord = params['discord']
	
	@bot.slash_command(name="channel")
	async def channel(inter):
		pass

	@channel.sub_command(name = "hide")
	async def tc_hide_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unhide:int = 0):
		"""
		Hide/Unhide channel for a role
		Parameters
		----------
		channel: target channel/category
		role: role to be affected by the change
		unhide: display the channel/category for the role - enter 1 to activate (default 0)
		"""
		try:
			await toggle_hide_channel(channel, role, bool(unhide))
		except Exception as ex:
			print('----- /tc_hide_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_hide_channel', interaction)

	@channel.sub_command(name = "lock")
	async def tc_lock_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unlock:int = 0):
		"""
		Lock/Unlock channel for a role
		Parameters
		----------
		channel: target channel
		role: role to be affected by the change
		unlock: unlock the channel/category for the role - enter 1 to activate (default 0)
		"""
		try:
			await toggle_lock_channel(channel, role, bool(unlock))
		except Exception as ex:
			print('----- /tc_lock_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_lock_channel', interaction)

	@channel.sub_command(name = "voice-clone")
	async def clone_voice_channel(interaction, channel:discord.VoiceChannel, name = None):
		"""
		Clone a voice channel
		Parameters
		----------
		channel: Voice channel to clone
		name: Channel name (optional)
		"""
		try:
			excludedCategories = [
				categories['voice-channels'],
				categories['help-voice'],
			]
			if channel.category_id not in excludedCategories:
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Cloning...', ephemeral=True)
			if (name == None) or (name == channel.name):
				name = f'{channel.name} / (cloned)'
			await channel.clone(name = name)
		except Exception as ex:
			print('----- /clone_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/clone_voice_channel', interaction)

	@channel.sub_command(name = "voice-delete")
	async def delete_voice_channel(interaction, channel:discord.VoiceChannel):
		"""
		Delete a voice channel
		Parameters
		----------
		channel: Voice channel to delete
		"""
		try:
			excludedCategories = [
				categories['voice-channels'],
				categories['help-voice'],
			]
			if (channel.category_id not in excludedCategories) or (channel.id in protected_voiceChannels):
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Deleting...', ephemeral=True)
			await channel.delete()
		except Exception as ex:
			print('----- /delete_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/delete_voice_channel', interaction)
