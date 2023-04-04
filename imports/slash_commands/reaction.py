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
	async def tc_update_roles_reactions(interaction, channel:discord.TextChannel, msg_id):
		"""
		Update existing role-reactions in case the bot was offline
		Parameters
		----------
		channel: Targer channel
		msg_id: Message target ID
		"""
		try:
			msg = await channel.fetch_message(int(msg_id))
			roles_assigned = 0
			_msg = ''
			for r in msg.reactions:
				roleName = reactions[str(channel.id)][str(msg_id)][str(r.emoji)]
				role = discord.utils.get(interaction.guild.roles, name = roleName)
				reacted_users = await r.users().flatten()
				for u in reacted_users:
					try:
						if u.id != users['teabot']:
							member = await interaction.guild.fetch_member(u.id)
							if role not in member.roles:
								await member.add_roles(role)
								_msg += f'{member.display_name}#{member.discriminator} got {role.mention}\n'
								_msg += f'Member ID : {member.id} / {member.mention}\n'
								roles_assigned += 1
					except Exception as ex:
						print('---------- /update_msg_reactions()/add role user --------')
						print(ex)
						await msg.remove_reaction(r.emoji, u)
						await log_exception(ex, '/update_msg_reactions()/add role user', interaction, msg=f'user : {u.mention} / role : {role.mention}')
						pass
			
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
			