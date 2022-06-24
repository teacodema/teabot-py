import json
import os
from setup.data.properties import *
from setup.actions.common import *
from setup.actions.role import *

def init_slash_commands_role(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name = "tc_tr", description = "Toggle role to member/role")
	async def toggle_role(interaction, role: discord.Role, member: discord.Member = None, role2: discord.Role = None, assign:int = 1):
		try:

			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return

			await interaction.send('Toggling Role...', ephemeral=True)
			msg = ''
			if role2:
				msg += f'{role2.mention} {"got" if assign else "lost"} a role : {role.mention}\n'
				members = role2.members
				for memberTo in members:
					await toggleRole(memberTo, [role], assign, interaction)
			if member == None and role2 == None:
				member = interaction.author
				await toggleRole(member, [role], assign, interaction)
				msg += f'{member.mention} {"got" if assign else "lost"} a role : {role.mention}\n'
			if member:
				await toggleRole(member, [role], assign, interaction)
				msg += f'{member.mention} {"got" if assign else "lost"} a role : {role.mention}\n'

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
					await toggleRole(m, roles_list, assign, interaction)
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


	@bot.slash_command(name = "tc_hr", description = "Member has(n't) role")
	async def members_has_role(interaction, role: discord.Role, has: int=1):
		try:
			
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
			
			await interaction.send('Searching...', ephemeral=True)
			guild = interaction.guild
			if has:
				verb = "have"
				filtered = filter(lambda member: member.get_role(role.id) != None, guild.members)
			else:
				verb = "don't have"
				filtered = filter(lambda member: member.get_role(role.id) == None, guild.members)
			filtered = list(filtered)
			
			count = len(filtered)
			msg = f"These members({count}) {verb} this role {role.mention}\n"
			if count <= 100:
				for member in filtered:
					msg += f'{member.mention} , '
				await interaction.send(msg.strip(), ephemeral=True)
			else:
				json_filtered = []
				for member in filtered:
					json_filtered.append({"id":member.id, "name":member.name})
				json_data = json.dumps(json_filtered)
				with open("file.json", "w") as outfile:
					outfile.write(json_data)
				file = discord.File("file.json")
				await interaction.send(content=msg, file=file, ephemeral=True)
				os.remove("file.json")

		except Exception as ex:
			print('----- /members_hasnt_role() -----')
			print(ex)
			await log_exception(ex, '/members_hasnt_role', interaction)


