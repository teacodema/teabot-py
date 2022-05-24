from setup.properties import *
from setup.actions import *

def init_server_activity(params):
	
	discord = params['discord']
	bot = params['bot']
	

	@bot.event
	async def on_member_update(before, after):
		try:
			if (after.id == users['drissboumlik']):
				return
			else:
				new = after.nick
				if (new):
					new = new.lower()
					old = before.nick
					allowed = False
					allowed = new.count('boumlik') or new.count('teacode') or new.count('teabot')
					if (allowed):
						if (old):
							await after.edit(nick = old)
						else:
							await after.edit(nick = "STOP THAT")
						
		except Exception as ex:
			print('----- on_member_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_update(evt)', None, bot)

	######################## JOIN MEMBER ########################
	@bot.event
	async def on_member_join(member):
		try:
			if member.bot:
				await member.kick(reason=f"Kicked a bot (ID: {member.id})")
				return
			msg = await welcomeMember(member, 1, 1, 0)
			channel = bot.get_channel(textChannels['log-server'])
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_join(evet) -----')
			print(ex)
			await log_exception(ex, 'on_member_join(evet)', None, bot)
		

	######################## REMOVE MEMBER ########################
	@bot.event
	async def on_member_remove(member):
		try:
			if member.bot:
				channel = bot.get_channel(textChannels['log-server'])
				await channel.send(f"🤖 kicked a bot (ID: {member.id})")
				return
			membersCount = await updateMembersCount(member)
			channel = bot.get_channel(textChannels['log-server'])
			_name = replace_str(member.name, {"_": "\_", "*": "\*"})
			_display_name = replace_str(member.display_name, {"_": "\_", "*": "\*"})
			msg = f'🟥 **{membersCount}** - {member.mention} / [{_name}#{member.discriminator}] / ({_display_name}) / ({member.id}) left **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_remove(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_remove(evt)', None, bot)

	######################## WELCOME MEMBER CMD ########################
	@bot.slash_command(name = "tc_w", description = "Welcome non-activated users")
	async def welcome(interaction, member: discord.Member, assign_role: int=0, send_dm: int=0, use_webhook: int=0):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
				
			await interaction.send(f'Welcoming {member.mention}', ephemeral=True)
			msg = await welcomeMember(member, assign_role, send_dm, use_webhook)
			channel = bot.get_channel(textChannels['log-server'])			
			await channel.send(msg)
		except Exception as ex:
			print('----- /welcome() -----')
			print(ex)
			await log_exception(ex, '/welcome', interaction)

	######################## WELCOME MEMBER ########################
	async def welcomeMember(member, assign_role = 0, send_dm = 0, use_webhook = 0):
		try:
			channel = bot.get_channel(textChannels['log-server'])
			msg = ''
			if int(use_webhook):
				wh_made = await make_webhook(member, channel)
				if wh_made: msg += '\n✅ Webhook made'
				else: msg += '\n❌ Webhook not made' 
			if int(assign_role):
				assigned = await assign_init_roles(member)
				if assigned: msg += "\n🟢 initial roles assigned 🎭"
				else: msg += "\n🔴 initial roles assigned 🎭"
			if int(send_dm):
				dm_sent = await send_dm_welcome(member)
				if dm_sent: msg +=f'\n📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
				else: msg += f'\n❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
			membersCount = await updateMembersCount(member)
			_name = replace_str(member.name, {"_": "\_", "*": "\*"})
			_display_name = replace_str(member.display_name, {"_": "\_", "*": "\*"})
			msg += f'\n🟩 **{membersCount}** - {member.mention} / [{_name}#{member.discriminator}] / ({_display_name}) / ({member.id}) join **TeaCode**'
			return msg
		except Exception as ex:
			print('----- welcomeMember() -----')
			print(ex)
			await log_exception(ex, 'welcomeMember()', None, bot)
			return 0

	async def send_dm_welcome(member):
		try:
			startHereChannel = bot.get_channel(textChannels['start-here'])
			invite = await startHereChannel.create_invite(max_age=appParams['inviteMaxAge'], max_uses=appParams['inviteMaxUses'], reason='Welcoming member')
			message = f'Merhba bik m3ana {member.mention} f **TeaCode** Community :flag_ma: :partying_face: :tada: '
			message += f"\n\nHna ghadi tl9a chno tehtaj bach takhod fikra 3la server ➜ <#{textChannels['start-here']}>"
	
			message += f"\nSowwel hna ➜ <#{textChannels['ask-staff']}> ila htajiti chi haja f server."
			message += f"\nDon't forget to **invite** your friends who could be interested {invite}"
			message += f"\n\n➜ Ila ma3reftich chno dir t9der tsowwel <@{users['drissboumlik']}>"
	
			channel = await member.create_dm()
			await channel.send(message)
			return 1
		except Exception as ex:
			print('----- send_dm_welcome() -----')
			print(ex)
			await log_exception(ex, 'send_dm_welcome()', None, bot)
			return 0
				
	async def make_webhook(member, channel):
		try:
			webhook = await channel.create_webhook(name=member.name)
			await webhook.send(f'Hi I\'m {member.display_name}/{member.mention}', username=member.name, avatar_url=member.avatar_url)
			await webhook.delete()
			return 1
		except Exception as ex:
			print('----- make_webhook() -----')
			print(ex)
			await log_exception(ex, 'make_webhook()', None, bot)
			return 0

	######################## UPDATE MEMBERS COUNT ########################
	async def updateMembersCount(member):
		try:
			guild = bot.get_guild(guildId)
			memberList = guild.members
			membersCount = len(memberList)
			return membersCount
		except Exception as ex:
			print('----- updateMembersCount() -----')
			print(ex)
			await log_exception(ex, 'updateMembersCount()', None, bot)

	async def assign_init_roles(member):
		try:
			_roles = [
				roles['new-members'], roles['members'],
				roles['__server_activities__'],
				roles['__techs__'], roles['__tools__'],
				roles['__jobs__'], roles['__interests__'],
			]
			roles_list = []
			guild = bot.get_guild(guildId)
			for role_id in _roles:	
				role = guild.get_role(role_id)
				roles_list.append(role)
			await member.add_roles(*roles_list)

			# @tasks.loop(minutes=1, count=2, reconnect=True)
			# async def give_role_member():
			# 	if give_role_member.current_loop == 0:
			# 		role = get(guild.roles, id = roles['members'])
			# 		await member.add_roles(role)
			# give_role_member.start()
			return 1
		except Exception as ex:
			print('----- assign_init_roles() -----')
			print(ex)
			await log_exception(ex, 'assign_init_roles()', None, bot)
			return 0