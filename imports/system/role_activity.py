from setup.properties import *
from setup.actions import *

def init_role_activity(params):
	
	bot = params['bot']
	discord = params['discord']	

	######################## TOGGLE ADD ########################
	@bot.slash_command(name = "tc_tr", description = "Toggle role to member/role")
	async def toggle_role(interaction, role: discord.Role, member: discord.Member = None, role2: discord.Role = None, assign:int = 1):
		try:

			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return

			await interaction.send('Toggling Role...', ephemeral=True)
			if (role2 != None and member == None):
				msg = f'{role2.mention} {"got" if assign else "lost"} a role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(interaction, memberTo, [role], assign)
			else:
				if (not member):
					member = interaction.author
				await toggleRole(interaction, member, [role], assign)
				msg = f'{member.mention} {"got" if assign else "lost"} a role : {role.mention}'

			await interaction.send(msg, ephemeral=True)
		except Exception as ex:
			print('----- /toggle_role() -----')
			print(ex)
			await log_exception(ex, '/toggle_role', interaction)


	######################## ROLE TO MEMBERS ########################
	@bot.slash_command(name = "tc_trm", description = 'Toggle multiple roles to multiple members - ,')
	async def toggle_role_members(interaction, roles, members, assign: int = 1):
		try:
			
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
			
			await interaction.send('Updating Role...', ephemeral=True)
			guild = bot.get_guild(guildId)

			msg_r = ''
			roles = roles.split(',')
			roles_list = []
			for role_id in roles:
				role_id = role_id.replace('<@&', '')
				role_id = role_id.replace('>', '')
				role = guild.get_role(int(role_id))
				msg_r += f'{role.mention}, '
				roles_list.append(role)

			msg_m = ''
			members = members.split(',')
			for m in members:
				try:
					m = m.replace('<@!', '')
					m = m.replace('>', '')
					m = await guild.fetch_member(m)
					msg_m += f'{m.mention}, '
					await toggleRole(interaction, m, roles_list, assign)
				except Exception as ex:
					print('----- /toggle_role_members()/toggle member -----')
					print(ex)
					pass

			msg = f'{msg_m} {"got" if assign else "lost"} roles : {msg_r}'
			await interaction.send(msg, ephemeral=True)
		except Exception as ex:
			print('----- /toggle_role_members() -----')
			print(ex)
			await log_exception(ex, '/toggle_role_members', interaction)


	######################## TOGGLE ROLE ########################
	async def toggleRole(interaction, member, roles, assign = True):
		try:
			if assign:
				await member.add_roles(*roles)
			else:
				await member.remove_roles(*roles)
		except Exception as ex:
			print('----- toggleRole() -----')
			print(ex)
			await log_exception(ex, 'toggleRole()', interaction)