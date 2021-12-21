from setup.properties import *
from setup.actions import *
import time

def init_server_activity(params):
	
	discord = params['discord']
	bot = params['bot']
	slash = params['slash']
	tasks = params['tasks']
	get = params['get']
	

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
					allowed = new.count('boumlik')
					if (allowed):
						if (old):
							await after.edit(nick = old)
						else:
							await after.edit(nick = "STOP THAT")
						
		except Exception as ex:
			print('----- on_member_update(evt) -----')
			print(ex)	

	######################## JOIN MEMBER ########################
	@bot.event
	async def on_member_join(member):
		try:
			if (member.bot == False):
				memberType = 'Human'
			else:
				memberType = 'Bot'
			message = await welcomeMember(member, 1)
			if (message == -1):
				msg = f'❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator} ({memberType})**'
			else:
				msg = f'📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator} ({memberType})**'
			membersCount = await updateMembersCount(member)
			channel = bot.get_channel(textChannels['log-server'])
			msg += f'\n:green_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) join **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_join(evet)/DM -----')
			print(ex)

		try:
			_roles = [
				roles['new-members'],
				roles['techs'], roles['tools'],
				roles['jobs'], roles['interests'],
			]
			roles_list = []
			guild = bot.get_guild(guildId)
			for role_id in _roles:	
				role = get(guild.roles, id = role_id)
				roles_list.append(role)
			await member.add_roles(*roles_list)
			# time.sleep(5)

			@tasks.loop(minutes=1, count=2, reconnect=True)
			async def give_role_member():
				if give_role_member.current_loop == 0:
					role = get(guild.roles, id = roles['members'])
					await member.add_roles(role)
			give_role_member.start()

		except Exception as ex:
			print('----- on_member_join(evt) -----')
			print(ex)
		

	######################## REMOVE MEMBER ########################
	@bot.event
	async def on_member_remove(member):
		try:
			membersCount = await updateMembersCount(member)
			channel = bot.get_channel(textChannels['log-server'])
			msg = f':red_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) left **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_remove(evt) -----')
			print(ex)

	######################## WELCOME MEMBER CMD ########################
	@slash.slash(name="w", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def welcome(ctx, member: discord.Member, use_webhook: int=0):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			await ctx.send(f'Msg sent to {member.mention}', hidden=True)
			message = await welcomeMember(member, use_webhook)

			if (message == -1):
				msg = f'❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
			else:
				msg = f'📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
			membersCount = await updateMembersCount(member)
			channel = bot.get_channel(textChannels['log-server'])
			msg += f'\n:green_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) join **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- /welcome() -----')
			print(ex)

	######################## WELCOME MEMBER ########################
	async def welcomeMember(member, use_webhook = 0):
		try:
			
			if int(use_webhook):
				try:
					channel = bot.get_channel(textChannels['log-server'])
					webhook = await channel.create_webhook(name=member.name)
					await webhook.send(f'Hi I\'m {member.display_name}/{member.mention}', username=member.name, avatar_url=member.avatar_url)
					await webhook.delete()
				except Exception as ex:
					print('----- /welcomeMember()/webhook-----')
					print(ex)

			message = f'Merhba bik m3ana {member.mention} f **TeaCode Community** :partying_face:\t:tada: '
			message += f"\nHna ghadi tl9a chno tehtaj bach takhod fikra 3la server <#{textChannels['first-steps']}>"

			message += f"\n\nAsk here <#{textChannels['ask-staff']}> if you need help with the server."
			message += "\nDon't forget to **invite** your friends who could be interested https://discord.gg/vKu2fkPqjY"

			channel = await member.create_dm()
			await channel.send(message)
			return message
		except Exception as ex:
			print('----- welcomeMember() -----')
			print(ex)
			return -1


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
