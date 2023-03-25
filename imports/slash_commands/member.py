import random
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
		assign_role: Assign initial roles - enter 1 to activate (default 0)
		send_dm: Send a dm - enter 1 to activate (default 0)
		use_webhook: Make a webhook for the new member - enter 1 to activate (default 0)
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
		do: Apply the update - enter 1 to activate (default 0)
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
		do: Apply the update - enter 1 to activate (default 0)
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
	