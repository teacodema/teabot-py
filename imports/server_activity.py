import time
from setup.properties import *
from setup.actions import *

def init_server_activity(params):
	
	discord = params['discord']
	client = params['client']
	slash = params['slash']
	get = params['get']

	@client.event
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
	@client.event
	async def on_member_join(member):

		try:
			if (member.bot == False):
				message = await welcomeMember(member)
				msg = 'Human'
			else:
				msg = 'Bot'
			channel = client.get_channel(textChannels['log-server'])
			if (message == -1):
				await channel.send(f'❗ DM/ Welcome Message --> Member: **{member.name}#{member.discriminator} ({msg})**')
			else:
				await channel.send(f'📨 DM/ Welcome Message --> Member: **{member.name}#{member.discriminator} ({msg})**')
			await updateMembersCount(member, client, True)
		except Exception as ex:
			print('----- on_member_join -----')
			print(ex)
		try:
			await validateMemeber(member, roles['new-members'], client, get)
			time.sleep(30)
			await validateMemeber(member, roles['members'], client, get)
			await validateMemeber(member, roles['skills'], client, get)
		except Exception as ex:
			print('----- on_member_join -----')
			print(ex)


	######################## REMOVE MEMBER ########################
	@client.event
	async def on_member_remove(member):
		try:
			await updateMembersCount(member, client, False)
		except Exception as ex:
			print('----- on_member_remove -----')
			print(ex)


	@slash.slash(name="welcome", guild_ids=[guildId])
	async def welcome(ctx, member: discord.Member):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
				
			await ctx.send(f'Msg sent to {member.mention}', delete_after = 2)
			
			message = await welcomeMember(member)
			
			channel = client.get_channel(textChannels['log-channel'])
			if (message == -1):
				await channel.send(f'❗ DM/ Welcome Message --> Member: **{member.name}#{member.discriminator}**')
			else:
				await channel.send(f'📨 DM/ Welcome Message --> Member: **{member.name}#{member.discriminator}**')
		except Exception as ex:
			print('----- /welcome -----')
			print(ex)


async def welcomeMember(member):

	try:
		channel = await member.create_dm()

		message = f'Merhba {member.mention} bik m3ana f **TeaCode Community** :partying_face: :tada: '
		message += "\nWhere We help/support **Moroccans** programming beginners :computer: in their learning journey :rocket:"
		
		message += "\n\nFollow the steps to **know** the rules & **see** the hidden rooms :warning:"
		message += "\nIf you're **new** to discord check this video https://teacode.ma/about :bangbang:"


		message += "\n\n**0┊Activate your membership**"
		message += f"\n   **・**Read & React to the <#{textChannels['rules']}> to be a verified **@Members**."

		message += "\n\n**1┊Go to**"
		message += f"\n   **・**<#{textChannels['get-roles']}> and react to get your skills roles."
		message += f"\n   **・**<#{textChannels['faqs']}> where you can find answers to common questions about the server."
		message += f"\n   **・**<#{textChannels['introduce-yourself']}> if you want to Introduce yourself . (First name, age, school .... etc)."

		message += "\n\n**2┊Need Help ?**"
		message += f"\n   **・**Ask the **@Moderators**/**@Staff** guys here <#{textChannels['ask-staff']}> if you need help with the server."

		message += "\n\n**3┊Links**"
		message += "\n   **・**Website : <https://teacode.ma>"
		message += "\n   **・**Discord : https://discord.gg/vKu2fkPqjY"
		message += "\n   **・**Facebook : <https://teacode.ma/facebook>"
		message += "\n   **・**Youtube : <https://teacode.ma/youtube>"
		message += "\n   **・**Instagram : <https://teacode.ma/instagram>"
		message += "\n   **・**Twitter : <https://teacode.ma/twitter>"

		message += "\n\n**4┊How To Support us**"
		message += "\n   **・**Paypal : <https://teacode.ma/paypal>"
		message += "\n   **・**Patreon : <https://teacode.ma/patreon>"
	
		await channel.send(message)
		return message
	except Exception as ex:
		print('----- welcomeMember -----')
		print(ex)
		return -1

######################## ON JOIN SERVER ########################
async def validateMemeber(member, roleId, client, get):
	try:
		guild = client.get_guild(guildId)
		role = get(guild.roles, id = roleId)
		await member.add_roles(role)
	except Exception as ex:
		print('----- validateMemeber -----')
		print(ex)


######################## ON JOIN SERVER ########################
async def updateMembersCount(member, client, join = True):
	try:
		guild = client.get_guild(guildId)
		memberList = guild.members
		membersCount = len(memberList)

		logServerActivity = client.get_channel(textChannels['log-server'])
		if (join):
			await logServerActivity.send(f':green_square: **{membersCount}** - {member.mention} | *{member.name}#{member.discriminator}* | **{member.display_name}** join **TeaCode**')
		else:
			await logServerActivity.send(f':red_square: **{membersCount}** - {member.mention} | *{member.name}#{member.discriminator}* | **{member.display_name}** left **TeaCode**')
	except Exception as ex:
		print('----- updateMembersCount -----')
		print(ex)

