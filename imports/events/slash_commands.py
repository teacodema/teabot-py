from imports.actions.message import *
from imports.data.properties import *

def init_events_slash_commands(params):

	bot = params['bot']

	@bot.slash_command_check
	async def check_slash_command(interaction):
		# print(inter.application_command.name)
		# print(inter.application_command.callback.__name__)
		await interaction.send(f"<@{users['teabot']}> is thinking...", ephemeral=True)
		action_name = interaction.application_command.callback.__name__
		if not is_allowed(interaction, action_name):
			await interaction.send('❌ Missing Permissions', ephemeral=True)
			return False
		await interaction.channel.trigger_typing()
		return True

	@bot.listen()
	async def on_slash_command(interaction):
		msg = '──────────────────────'
		msg += '\n------- on_slash_command -------'
		msg += f'\nCommand : {interaction.application_command.name} / {interaction.application_command.callback.__name__}'
		msg += f'\nDescription : {interaction.application_command.body.description}'
		msg += f'\nChannel : {interaction.channel.mention}'
		user_mention = await toggle_user_mention(bot, interaction.author, roles['root'], True)
		msg += f'\nAuthor : {user_mention}'
		msg += '\nParameters'
		params = interaction.filled_options
		paramskeys = params.keys()
		for key in paramskeys:
			msg += f'\n\t- {key} : {params[key]}'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())

	@bot.listen()
	async def on_slash_command_completion(interaction):
		await interaction.send(f"<@{users['teabot']}> is done.", ephemeral=True)
		msg = '------- on_slash_command_completion -------'
		msg += '\nCompleted'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())
		
	@bot.listen()
	async def on_slash_command_error(interaction, exception):
		msg = '------- on_slash_command_error -------'
		msg += '\nError'
		msg += f'\n{str(exception)}'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())