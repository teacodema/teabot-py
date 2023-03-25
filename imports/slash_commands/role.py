import json, os
from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.role import *

def init_slash_commands_role(params):
	
	bot = params['bot']
	discord = params['discord']
	
	@bot.slash_command(name="role")
	async def role(inter):
		pass
	
	@role.sub_command(name = "fetch")
	async def tc_roles_fetch(interaction, sort_by_count:int = 0):
		"""
		Fetch roles data
		Parameters
		----------
		sort_by_count: members count - enter 1 to activate (default 0)
		"""
		try:
			roles = interaction.guild.roles
			if sort_by_count: roles = sorted(roles, key=lambda role: len(role.members))
			list = []
			for role in roles:
				object = {"id":role.id, "name":role.name, "position":role.position, "count": len(role.members)}
				list.append(object)
			json_data = json.dumps(list)
			with open("file.json", "w") as outfile:
				outfile.write(json_data)
			file = discord.File("file.json")
			await interaction.send(file=file, ephemeral=True)
			os.remove("file.json")
		except Exception as ex:
			print('----- /tc_roles_fetch() -----')
			print(ex)
			await log_exception(ex, '/tc_roles_fetch', interaction)
	
	################## UPDATE ROLE ####################
	@role.sub_command(name = "update-position")
	async def tc_update_roles_position(interaction, roles, role:discord.Role):
		"""
		Update role position - ,
		Parameters
		----------
		roles: Role to update separated by , or space
		role: positionned at "role.position - 1" / @everyone = 0
		"""
		try:
			guild = interaction.guild
			msg_r = ''
			roles = split_str(roles)
			roles.reverse()
			position = role.position
			for role_id in roles:
				role_id = role_id.replace('<@&', '').replace('>', '')
				_role = guild.get_role(int(role_id))
				await _role.edit(position=position)
				msg_r += f'{_role.mention}, '

			msg = f"Roles position updated {msg_r} under {role.mention}"
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /tc_update_roles_position() -----')
			print(ex)
			await log_exception(ex, '/tc_update_roles_position', interaction)

	
	@role.sub_command(name = "toggle")
	async def tc_toggle_role(interaction, role: discord.Role, member: discord.Member = None, role2: discord.Role = None, assign:int = 1):
		"""
		Toggle role to member/role
		Parameters
		----------
		role: Role to toggle
		member: Member the role will be toggled to
		role2: Role members the role will be toggled to
		assign: Assign/Unassign - values 0/1 - default 1
		"""
		try:
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

			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /tc_toggle_role() -----')
			print(ex)
			await log_exception(ex, '/tc_toggle_role', interaction)

	######################## ROLE TO MEMBERS ########################
	@role.sub_command(name = "toggle-multiple")
	async def tc_toggle_roles_members(interaction, roles, members, assign: int = 1):
		"""
		Toggle multiple roles to multiple members - ,
		Parameters
		----------
		roles: Roles to toggle separated by , or space
		members: Members the roles will be toggled to separated by , or space
		assign: Assign/Unassign - values 0/1 - default 1
		"""
		try:
			guild = bot.get_guild(guildId)

			msg_r = ''
			roles = split_str(roles)
			roles_list = []
			for role_id in roles:
				role_id = role_id.replace('<@&', '').replace('>', '')
				role = guild.get_role(int(role_id))
				msg_r += f'{role.mention}, '
				roles_list.append(role)

			msg_m = ''
			members = split_str(members)
			for m in members:
				try:
					m = m.replace('<@!', '').replace('<@', '').replace('>', '')
					m = await guild.fetch_member(m)
					msg_m += f'{m.mention}, '
					await toggleRole(m, roles_list, assign, interaction)
				except Exception as ex:
					print('----- /toggle_role_members()/toggle member -----')
					print(ex)
					pass

			msg = f'{msg_m} {"got" if assign else "lost"} roles : {msg_r}'
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /tc_toggle_roles_members() -----')
			print(ex)
			await log_exception(ex, '/tc_toggle_roles_members', interaction)

	@role.sub_command(name = "has")
	async def tc_members_has_role(interaction, role: discord.Role, has: int=1):
		"""
		Members who have(n't) a role
		Parameters
		----------
		role: Role to check
		has: Check for having/not having - values 0/1 - default 1
		"""
		try:
			guild = interaction.guild
			if has:
				verb = "have"
				filtered_members = filter(lambda member: member.get_role(role.id) != None, guild.members)
			else:
				verb = "don't have"
				filtered_members = filter(lambda member: member.get_role(role.id) == None, guild.members)
			filtered_members = list(filtered_members)
			
			count = len(filtered_members)
			msg = ''
			# send_file = False
			# MAX_COUNT = 50
			for member in filtered_members:
				msg += f'{member.mention} , '
				if len(msg) > 1800:
					await interaction.send(msg.strip(), ephemeral=True)
					msg = ''
			msg += f"\n\nThese members({count}) {verb} this role {role.mention}\n"
			await interaction.send(msg.strip(), ephemeral=True)
			# if count > MAX_COUNT:
			# 	send_file = True
			# else:
			# 	for member in filtered_members:
			# 		msg += f'{member.mention} , '
			# 	if len(msg) >= 2000: send_file = True
			
			# if not send_file:
			# 	await interaction.send(msg.strip(), ephemeral=True)
			# else:
			# 	json_filtered_members = []
			# 	for member in filtered_members:
			# 		object = {"id":member.id, "name":member.name , "mention": member.mention, "display_name": member.display_name}
			# 		json_filtered_members.append(object)
			# 	json_data = json.dumps(json_filtered_members)
			# 	with open("file.json", "w") as outfile:
			# 		outfile.write(json_data)
			# 	file = discord.File("file.json")
			# 	await interaction.send(content=msg.strip(), file=file, ephemeral=True)
			# 	os.remove("file.json")

		except Exception as ex:
			print('----- /tc_members_has_role() -----')
			print(ex)
			await log_exception(ex, '/tc_members_has_role', interaction)
