from setup.properties import *
from setup.actions import *
import time

def init_server_activity(params):
	
	discord = params['discord']
	bot = params['bot']
	slash = params['slash']
	get = params['get']
	create_permission = params['create_permission']
	SlashCommandPermissionType = params['SlashCommandPermissionType']

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
			print('----- on_member_update -----')
			print(ex)	

	######################## JOIN MEMBER ########################
	@bot.event
	async def on_member_join(member):
		try:
			if (member.bot == False):
				memberType = 'Human'
			else:
				memberType = 'Bot'
			message = await welcomeMember(member)
			if (message == -1):
				msg = f'❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator} ({memberType})**'
			else:
				msg = f'📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator} ({memberType})**'
			membersCount = await updateMembersCount(member, bot)
			channel = bot.get_channel(textChannels['log-server'])
			msg += f'\n:green_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) join **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_join 1-----')
			print(ex)
	
		# try:
		# 	webhook = await channel.create_webhook(name=member.name)
		# 	await webhook.send(f'Hi I\'m {member.display_name}', username=member.name, avatar_url=member.avatar_url)
		# 	await webhook.delete()
		# except Exception as ex:
		# 	print('----- on_member_join 3-----')
		# 	print(ex)

		try:
			await validateMemeber(member, roles['new-members'], bot, get)
			time.sleep(120)
			_roles = [
				roles['members'],
				roles['techs'], roles['tools'],
				roles['jobs'], roles['interests'],
			]
			for rold_id in _roles:
				await validateMemeber(member, rold_id, bot, get)
		except Exception as ex:
			print('----- on_member_join 2-----')
			print(ex)
		

	######################## REMOVE MEMBER ########################
	@bot.event
	async def on_member_remove(member):
		try:
			membersCount = await updateMembersCount(member, bot)
			channel = bot.get_channel(textChannels['log-server'])
			msg = f':red_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) left **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_remove -----')
			print(ex)

	######################## WELCOME MEMBER CMD ########################
	# @bot.command(name="welcome", pass_context=True)
	@slash.slash(name="welcome", guild_ids=[guildId],
		permissions={ guildId: [ 
				create_permission(roles['members'], SlashCommandPermissionType.ROLE, False),
				create_permission(roles['everyone'], SlashCommandPermissionType.ROLE, False)
			]})
	async def welcome(ctx, member: discord.Member):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			await ctx.send(f'Msg sent to {member.mention}', delete_after = 2)
			message = await welcomeMember(member)
			if (message == -1):
				msg = f'❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
			else:
				msg = f'📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator}**'
			membersCount = await updateMembersCount(member, bot)
			channel = bot.get_channel(textChannels['log-server'])
			msg += f'\n:green_square: **{membersCount}** - {member.mention} | [{member.name}#{member.discriminator}] | ({member.display_name}) join **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- /welcome -----')
			print(ex)

######################## WELCOME MEMBER ########################
async def welcomeMember(member):
	try:
		message = f'Merhba {member.mention} bik m3ana f **TeaCode Community** :partying_face: :tada: '
		message += "\nWhere We help/support **Moroccans** programming beginners :computer: in their learning journey :rocket:"
		
		message += "\n\nFollow the steps to **know** the rules & **see** the hidden rooms :warning:"
		message += "\nIf you're **new** to discord check this video https://teacode.ma/about :bangbang:"
		message += "\nDon't forget to **invite** your friends who could be interested :speech_left:"

		message += "\n\n**0┊Activate your membership**"
		message += f"\n   **・**Read & React to the <#{textChannels['rules']}> to be a verified __**@Members**__."
		
		message += "\n\n**1┊Go to**"
		message += f"\n   **・**<#{textChannels['get-roles']}> and react to get your skills roles."
		message += f"\n   **・**<#{textChannels['faqs']}> where you can find answers to common questions about the server."
		message += f"\n   **・**<#{textChannels['introduce-yourself']}> if you want to Introduce yourself . (First name, age, school .... etc)."

		message += "\n\n**2┊Need Help ?**"
		message += f"\n   **・**Ask the __**@Moderators**__/__**@Staff**__ guys here <#{textChannels['ask-staff']}> if you need help with the server."

		message += "\n\n**3┊Links**"
		message += "\n   **・**Website : <https://teacode.ma>"
		message += "\n   **・**Discord : https://discord.gg/vKu2fkPqjY"
		message += "\n   **・**Facebook : <https://teacode.ma/facebook>"
		message += "\n   **・**YouTube : <https://teacode.ma/youtube>"
		message += "\n   **・**Instagram : <https://teacode.ma/instagram>"
		message += "\n   **・**Twitter : <https://teacode.ma/twitter>"

		message += "\n\n**4┊How To Support us**"
		message += "\n   **・**PayPal : <https://teacode.ma/paypal>"
		message += "\n   **・**Patreon : <https://teacode.ma/patreon>"
	
		channel = await member.create_dm()
		await channel.send(message)
		return message
	except Exception as ex:
		print('----- welcomeMember -----')
		print(ex)
		return -1

######################## VALIDATE MEMBER ########################
async def validateMemeber(member, roleId, bot, get):
	try:
		guild = bot.get_guild(guildId)
		role = get(guild.roles, id = roleId)
		await member.add_roles(role)
	except Exception as ex:
		print('----- validateMemeber -----')
		print(ex)


######################## UPDATE MEMBERS COUNT ########################
async def updateMembersCount(member, bot):
	try:
		guild = bot.get_guild(guildId)
		memberList = guild.members
		membersCount = len(memberList)
		return membersCount
	except Exception as ex:
		print('----- updateMembersCount -----')
		print(ex)
