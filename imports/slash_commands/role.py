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
		sort_by_count: members count - values 0/1 - default 0
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

