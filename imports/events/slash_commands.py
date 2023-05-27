from imports.actions.message import *
from imports.data_server.config import *

def init_events_slash_commands(params):

	bot = params['bot']

	@bot.slash_command_check
	async def check_slash_command(interaction):
		if interaction.application_command.parent == None:
			return True
		cmd_name = interaction.application_command.qualified_name
		if should_send_ephemeral_msg(cmd_name):
			await interaction.send(f"🔃 @teabot is thinking...", ephemeral=True)
		if not is_allowed(interaction, cmd_name):
			await interaction.send('❌ Missing Permissions', ephemeral=True)
			return False
		# await interaction.channel.trigger_typing()
		return True

	@bot.listen()
	async def on_slash_command(interaction):
		msg = '──────────────────────'
		msg += '\n------- on_slash_command -------'
		msg += f'\nCommand : {interaction.application_command.qualified_name} / {interaction.application_command.callback.__name__}'
		msg += f'\nDescription : {interaction.application_command.body.description}'
		msg += f'\nChannel : {interaction.channel.mention}'
		user_mention = await toggle_user_mention(bot, interaction.author, append_member_id = True)
		msg += f'\nAuthor : {user_mention}'
		msg += '\n- Parameters\n'
		params = interaction.filled_options
		paramskeys = params.keys()
		for key in paramskeys:
			msg += f'  - {key} : {params[key]}\n'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())

	@bot.listen()
	async def on_slash_command_completion(interaction):
		await interaction.send(f"✅ @teabot is done.", ephemeral=True)
		msg = '------- on_slash_command_completion -------'
		msg += '\nCompleted'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())
		
	@bot.listen()
	async def on_slash_command_error(interaction, exception):
		await interaction.send(f"⚠ @teabot had an issue.", ephemeral=True)
		msg = '------- on_slash_command_error -------'
		msg += '\nError'
		msg += f'\n{str(exception)}'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg.strip())