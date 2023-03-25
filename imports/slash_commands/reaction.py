from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.reaction import *

def init_slash_commands_reaction(params):

	bot = params['bot']
	discord = params['discord']


	@bot.slash_command(name="reaction")
	async def reaction(interaction):
		pass
	
	@reaction.sub_command(name = "toggle-roles")
	async def tc_update_roles_reactions(interaction, channel:discord.TextChannel = None, msg_id = None):
		"""
		Update existing role-reactions in case the bot was offline
		Parameters
		----------
		channel: Targer channel
		msg_id: Message target ID
		"""
		try:
			if channel and msg_id:
				returnedDict = await update_msg_reactions(params, interaction, channel, msg_id)
				roles_assigned = returnedDict['roles_assigned']
				_msg = returnedDict['_msg']
			else:
				roles_assigned = 0
				_msg = ''
				for channel_id in reactions:
					channel = bot.get_channel(int(channel_id))
					for msg_id in reactions[str(channel_id)]:
						await interaction.send(f'https://discord.com/channels/{guildId}/{channel_id}/{msg_id}', ephemeral=True)
						returnedDict = await update_msg_reactions(params, interaction, channel, msg_id)
						roles_assigned += returnedDict['roles_assigned']
						_msg += returnedDict['_msg']
			await interaction.send(f'Done Updating members roles / {roles_assigned} updated.\n{_msg}', ephemeral=True)
		except Exception as ex:
			print('---------- /tc_update_roles_reactions() --------')
			print(ex)
			await log_exception(ex, '/tc_update_roles_reactions', interaction)

	@reaction.sub_command(name = "toggle")
	async def tc_bot_react(interaction, msg_id, emojis, remove:int=0, member: discord.Member = None):
		"""
		Add/Remove reaction to/from msg - ,
		Parameters
		----------
		msg_id: Message ID
		emojis: Server existing emojis separated by , or space
		remove: Remove the reaction - enter 1 to activate (default 0)
		member: Member to remove reactions for (remove param should be == 1)
		"""
		try:
			msg = await interaction.channel.fetch_message(msg_id)
			emojis = split_str(emojis)
			for e in emojis:
				try:
					if remove:
						if member: await msg.remove_reaction(e, member)
						else: await msg.clear_reaction(e)
					else: await msg.add_reaction(e)
				except Exception as ex:
					print('---------- /tc_bot_react()/loop --------')
					print(ex)
					pass
		except Exception as ex:
			print('---------- /tc_bot_react() --------')
			print(ex)
			await log_exception(ex, '/tc_bot_react', interaction)
			