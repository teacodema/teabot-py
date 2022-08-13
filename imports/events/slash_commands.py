from setup.data.properties import *

def init_slash_commands_events(params):

	bot = params['bot']

	@bot.listen()
	async def on_slash_command(inter):
		msg = '-------on_slash_command-------'
		msg += f'\nCommand  : {inter.application_command.name} / {inter.application_command.qualified_name}'
		msg += f'\nChannel : {inter.channel.mention}'
		msg += f'\nAuthor : {inter.author.mention} / {inter.author.id}'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg)

	@bot.listen()
	async def on_slash_command_completion(inter):
		msg = '-------on_slash_command_completion-------'
		msg += '\nCompleted'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg)
		
	@bot.listen()
	async def on_slash_command_error(inter, exception):
		msg = '-------on_slash_command_error-------'
		msg += '\nError'
		msg += f'\n{str(exception)}'
		channel = bot.get_channel(textChannels['log-cmd'])
		await channel.send(msg)