from setup.data.params import *
from setup.actions.common import *

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
			await channel.clone(name = name)
		except Exception as ex:
			print('----- /clone_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/clone_voice_channel', interaction)
