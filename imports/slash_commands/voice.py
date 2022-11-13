from setup.data.params import *
from setup.actions.common import *
from setup.data.properties import *

def init_slash_commands_voice(params):
	bot = params['bot']
	discord = params['discord']
	inspect = params['inspect']
    
	@bot.slash_command(name = "clone-vc")
	async def clone_voice_channel(interaction, channel:discord.VoiceChannel, name = None):
		"""
		Clone a voice channel
		Parameters
		----------
		channel: Voice channel to clone
		name: Channel name (optional)
		"""
		try:
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			excludedCategories = [
				categories['voice-channels'],
				categories['help-voice'],
			]
			if channel.category_id not in excludedCategories:
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Cloning...', ephemeral=True)
			await channel.clone(name = name)
		except Exception as ex:
			print('----- /clone_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/clone_voice_channel', interaction)


	@bot.slash_command(name = "delete-vc")
	async def delete_voice_channel(interaction, channel:discord.VoiceChannel):
		"""
		Delete a voice channel
		Parameters
		----------
		channel: Voice channel to delete
		"""
		try:
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			if channel.id in protected_voiceChannels:
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Deleting...', ephemeral=True)
			await channel.delete()
		except Exception as ex:
			print('----- /delete_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/delete_voice_channel', interaction)
