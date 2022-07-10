from setup.data.params import * 
from setup.data.properties import *
from setup.actions.common import *

def init_slash_commands_reaction(params):

	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "tc_rr", description='')
	async def bot_react(interaction, msg_id=None, emojis=None, remove:int=0, member: discord.Member = None):
		"""
		Add/Remove reaction to/from msg - ,
		Parameters
		----------
		msg_id: Message ID
		emojis: Server existing emojis separated by , 
		remove: Remove the reaction - values 0/1
		member: Member to remove reactions for (remove param should be == 1)
		"""
		try:

			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
	
			if msg_id:
				if emojis:
					await interaction.send('Bot Reacting ....', ephemeral=True)
					msg = await interaction.channel.fetch_message(msg_id)
					emojis = emojis.split(',')
					for e in emojis:
						if remove:
							if member: await msg.remove_reaction(e, member)
							else: await msg.clear_reaction(e)
						else: await msg.add_reaction(e)
					return
				else:
					await interaction.send('Reactions are setting up ....', ephemeral=True)
					if str(interaction.channel.id) in reactions and str(msg_id) in reactions[str(interaction.channel.id)]:
						msg = await interaction.channel.fetch_message(msg_id)
						for e in reactions[str(interaction.channel.id)][msg_id]:
							await msg.add_reaction(e)
						await interaction.send('Done Reacting.', ephemeral=True)
					else: await interaction.send('Could not find channel/message.', ephemeral=True)
					return

			await interaction.send('Updating members roles ....', ephemeral=True)
			guild = bot.get_guild(guildId)
			roles_assigned = 0
			_msg = ''
			for channel_id in reactions:
				channel = bot.get_channel(int(channel_id))
				for msg_id in reactions[str(channel_id)]:
					try:
						msg = await channel.fetch_message(int(msg_id))
						for r in msg.reactions:
							roleName = reactions[str(channel_id)][str(msg_id)][str(r.emoji)]
							role = discord.utils.get(guild.roles, name = roleName)
							async for u in r.users():
								try:
									if u.id != users['teabot']:
										member = await guild.fetch_member(u.id)
										if role not in member.roles:
											await member.add_roles(role)
											_msg += f'{member.mention} got {role.mention}\n'
											roles_assigned += 1
								except Exception as ex:
									print('---------- /bot_react()/add role user --------')
									print(ex)
									print(role.name)
									print(u.name)
									await msg.remove_reaction(r.emoji, u)
									pass
					except Exception as ex:
						print('---------- /bot_react()/msg reactions --------')
						print(ex)
						print(channel.name)
						print(role.name)
						pass
			await interaction.send(f'Done Updating members roles / {roles_assigned} updated.\n{_msg}', ephemeral=True)
		except Exception as ex:
			print('---------- /bot_react() --------')
			print(ex)
			await log_exception(ex, '/bot_react', interaction)