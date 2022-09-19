import json
import os
from setup.data.properties import *
from setup.actions.common import *
from setup.actions.role import *

def init_slash_commands_role(params):
	
	bot = params['bot']
	discord = params['discord']
	inspect = params['inspect']

	@bot.slash_command(name = "tc_tr")
	async def toggle_role(interaction, role: discord.Role, member: discord.Member = None, role2: discord.Role = None, assign:int = 1):
		"""
		Toggle role to member/role
		Parameters
		----------
		role: Role to toggle
		member: Member the role will be toggled to
		role2: Role members the role will be toggled to
		assign: Assign/Unassign - values 0/1
		"""
		try:

			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
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
	@bot.slash_command(name = "tc_trm")
	async def toggle_role_members(interaction, roles, members, assign: int = 1):
		"""
		Toggle multiple roles to multiple members - ,
		Parameters
		----------
		roles: Roles to toggle separated by ,
		members: Members the roles will be toggled to separated by ,
		assign: Assign/Unassign - values 0/1
		"""
		try:
			
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
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


	@bot.slash_command(name = "tc_hr")
	async def members_has_role(interaction, role: discord.Role, has: int=1):
		"""
		Members who have(n't) a role
		Parameters
		----------
		role: Role to check
		has: Check for having/not having - values 0/1
		"""
		try:
			
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions')
				return
			
			await interaction.send('Searching...', ephemeral=True)
			guild = interaction.guild
			if has:
				verb = "have"
				filtered_members = filter(lambda member: member.get_role(role.id) != None, guild.members)
			else:
				verb = "don't have"
				filtered_members = filter(lambda member: member.get_role(role.id) == None, guild.members)
			filtered_members = list(filtered_members)
			
			count = len(filtered_members)
			msg = f"These members({count}) {verb} this role {role.mention}\n"
			send_file = False
			MAX_COUNT = 50
			if count > MAX_COUNT:
				send_file = True
			else:
				for member in filtered_members:
					msg += f'{member.mention} , '
				if len(msg) >= 2000: send_file = True
			
			if not send_file:
				await interaction.send(msg.strip(), ephemeral=True)
			else:
				json_filtered_members = []
				for member in filtered_members:
					object = {"id":member.id, "name":member.name , "mention": member.mention, "display_name": member.display_name}
					json_filtered.append(object)
				json_data = json.dumps(json_filtered_members)
				with open("file.json", "w") as outfile:
					outfile.write(json_data)
				file = discord.File("file.json")
				await interaction.send(content=msg, file=file, ephemeral=True)
				os.remove("file.json")

		except Exception as ex:
			print('----- /members_hasnt_role() -----')
			print(ex)
			await log_exception(ex, '/members_hasnt_role', interaction)


