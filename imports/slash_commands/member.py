from setup.data.properties import *
from setup.actions.common import *
from setup.actions.member import *

def init_slash_commands_member(params):
	
	bot = params['bot']
	discord = params['discord']	

	
	######################## WELCOME MEMBER CMD ########################
	@bot.slash_command(name = "tc_w")
	async def welcome(interaction, member: discord.Member, assign_role: int=0, send_dm: int=0, use_webhook: int=0):
		"""
		Welcome users manually (dm + assign initial roles)
		Parameters
		----------
		member: Server existing member
		assign_role: Assign initial roles - values 0/1
		send_dm: Send a dm - values 0/1
		use_webhook: Make a webhook for the new member - values 0/1
		"""
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
				
			await interaction.send(f'Welcoming {member.mention}', ephemeral=True)
			msg = await welcomeMember(params, member, assign_role, send_dm, use_webhook)
			channel = bot.get_channel(textChannels['log-server'])			
			await channel.send(msg)
		except Exception as ex:
			print('----- /welcome() -----')
			print(ex)
			await log_exception(ex, '/welcome', interaction)

	######################## CHECK UNASSIGNED MEMBERS ########################
	@bot.slash_command(name = "tc_cnm")
	async def check_new_members(interaction, nr:int=1, do:int=0):
		"""
		Check new membership period
		Parameters
		----------
		nr: Number of min roles - values 0 < nr
		do: Apply the update - values 0/1
		"""
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			await interaction.send('Checking ...', ephemeral=True)
			guild = interaction.guild
			if nr <= 0: nr = 1
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
	@bot.slash_command(name = "tc_unm")
	async def update_new_members(interaction, do:int=0):
		"""
		Check new-membership period
		Parameters
		----------
		do: Apply the update - values 0/1
		"""
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