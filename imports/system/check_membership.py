from setup.properties import *
from setup.actions import *


def init_check_membership(params):

	bot = params['bot']
	
	######################## CHECK UNASSIGNED MEMBERS ########################
	@bot.slash_command(name = "tc_cnm", description = "Check new membership period")
	async def check_new_members(interaction, nr:int=1, do:int=0):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			await interaction.send('Checking ...', ephemeral=True)
			guild = interaction.guild
			def count_roles(member):
				return (len(member.roles) <= nr + 1)
			users = list(filter(count_roles, guild.members))

			_roles = [
				roles['new-members'], roles['members'],
				roles['__server_activities__'],
				roles['__techs__'], roles['__tools__'],
				roles['__jobs__'], roles['__interests__'],
			]
			roles_list = []
			for role_id in _roles:	
				role = guild.get_role(role_id)
				roles_list.append(role)

			msg = ''
			for u in users:
				if do: await u.add_roles(*roles_list)
				msg += f'{u.mention} , '
			if do: await interaction.send(f'{len(users)} checked members.\n{msg}', ephemeral=True)
			else: await interaction.send(f'{len(users)} can be checked members.\n{msg}', ephemeral=True)

		except Exception as ex:
			print('----- /check_new_members() -----')
			print(ex)
			await log_exception(ex, '/check_new_members', interaction)


	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	@bot.slash_command(name = "tc_unm", description = "No longer new members")
	async def update_new_members(interaction, do:int=0):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			await interaction.send('Updating ...', ephemeral=True)
			updatedMembers = await checkNewMemberRole(interaction.guild, do)
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '
			if do: await interaction.send(f'{updatedMembersCount} updated members.\n{msg}', ephemeral=True)
			else: await interaction.send(f'{updatedMembersCount} can be updated members.\n{msg}', ephemeral=True)
		except Exception as ex:
			print('----- /update_new_members() -----')
			print(ex)
			await log_exception(ex, '/update_new_members', interaction)
