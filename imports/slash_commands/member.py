import json, os
from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.member import *

def init_slash_commands_member(params):
	
	bot = params['bot']
	discord = params['discord']	
	commands = params['commands']

	@bot.slash_command(name="member")
	async def member(inter):
		pass

	######################## WELCOME MEMBER CMD ########################
	@member.sub_command(name = "welcome")
	async def tc_welcome(interaction, member: discord.Member, assign_role: int=0, send_dm: int=0, use_webhook: int=0):
		"""
		Welcome users manually (dm + assign initial roles)
		Parameters
		----------
		member: Server existing member
		assign_role: Assign initial roles - values 0/1 - default 0
		send_dm: Send a dm - values 0/1 - default 0
		use_webhook: Make a webhook for the new member - values 0/1 - default 0
		"""
		try:
			msg = await welcomeMember(params, member, assign_role, send_dm, use_webhook)
			channel = bot.get_channel(textChannels['log-server'])			
			await channel.send(msg.strip())
		except Exception as ex:
			print('----- /tc_welcome() -----')
			print(ex)
			await log_exception(ex, '/tc_welcome', interaction)

	operators = ["less than", "more than"]
	######################## CHECK UNASSIGNED MEMBERS ########################
	@member.sub_command(name = "check-new")
	async def tc_check_new_members(interaction, operator = commands.Param(choices=operators), nr:int=1, do:int=0):
		"""
		Check new membership period
		Parameters
		----------
		nr: Number of min roles - values 0 < nr - default 1
		do: Apply the update - values 0/1 - default 0
		"""
		try:
			guild = interaction.guild
			if nr <= 0: nr = 1
			def count_roles(member):
				if operator == "less than": return (len(member.roles) < nr + 1)
				if operator == "more than": return (len(member.roles) > nr + 1)
			users = list(filter(count_roles, guild.members))

			_roles = [
				roles['new-members'], roles['members'],
				roles['__server_activities__'],
				roles['__techs_tools_jobs_interests__'],
			]
			roles_list = []
			for role_id in _roles:	
				role = guild.get_role(role_id)
				roles_list.append(role)

			msg = ''
			for u in users:
				if do: await u.add_roles(*roles_list)
				msg += f'{u.mention} , '
				if len(msg) > 1800:
					await interaction.send(msg, ephemeral=True)
					msg = ''
			if do: await interaction.send(f'{msg}\n{len(users)} checked members.', ephemeral=True)
			else: await interaction.send(f'{msg}\n{len(users)} can be checked members.', ephemeral=True)

		except Exception as ex:
			print('----- /tc_check_new_members() -----')
			print(ex)
			await log_exception(ex, '/tc_check_new_members', interaction)

	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	@member.sub_command(name = "update-new")
	async def tc_update_new_members(interaction, do:int=0):
		"""
		Check new-membership period
		Parameters
		----------
		do: Apply the update - values 0/1 - default 0
		"""
		try:
			updatedMembers = await checkNewMemberRole(interaction.guild, do)
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '
			if do: await interaction.send(f'{updatedMembersCount} updated members.\n{msg}', ephemeral=True)
			else: await interaction.send(f'{updatedMembersCount} can be updated members.\n{msg}', ephemeral=True)
		except Exception as ex:
			print('----- /tc_update_new_members() -----')
			print(ex)
			await log_exception(ex, '/tc_update_new_members', interaction)

	@member.sub_command(name = "toggle-role")
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
	@member.sub_command(name = "toggle-roles")
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

	@member.sub_command(name = "has-role")
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

	######### PICK RANDOM USER #######
	@member.sub_command(name = "pick-speaker", description = "Choose a random speaker - (events only !!)")
	async def pick_speaker(interaction):
		try:
			voice = interaction.author.voice
			if voice:
				members = voice.channel.members
				members = list(filter(is_not_host_or_bot, members))
				if len(members) == 0:
					msg = 'No member chosen !! - Reasons'
					msg+= '\n- No members available in the voice channel'
					msg+= '\n- Only hosts/bot are connected for now'
					await interaction.send(msg.strip(), ephemeral=True)
					return

				member = random.choice(members)
				msg = f'Chosen member : {member.mention}'
			else:
				msg = '⚠ No busy voice channel'
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /pick_speaker() -----')
			print(ex)
			await log_exception(ex, '/pick_speaker', interaction)


	####################### MAKE A WEBHOOK #######################
	@member.sub_command(name = "make-webhook")
	async def tc_make_webhook(interaction, member: discord.Member, channel: discord.abc.GuildChannel, msg, name=None):
		"""
		Make a webhook - \\n \\t /$
		Parameters
		----------
		member: Server existing member
		msg: Message to send by the webhook - \\n \\t /$
		channel: Channel where to send the msg
		name: Webhook name
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			if name == None:
				name = member.display_name
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})
			webhook = await channel.create_webhook(name=name)
			await webhook.send(f'{msg}', username=name, avatar_url=member.display_avatar.url)
			await webhook.delete()
			await interaction.send('✅ Webhook made', ephemeral=True)
		except Exception as ex:
			await interaction.send('❌ Webhook not made', ephemeral=True)
			print('----- /tc_make_webhook() -----')
			print(ex)
			await log_exception(ex, '/tc_make_webhook', interaction)
	