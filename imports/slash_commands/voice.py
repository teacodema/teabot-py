from imports.actions.common import *
from imports.data.server.config import *

def init_slash_commands_voice(params):
	bot = params['bot']
	discord = params['discord']
    
	@bot.slash_command(name = "voice-clone")
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


	@bot.slash_command(name = "voice-delete")
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
