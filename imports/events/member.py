import os
from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.member import *

def init_events_member(params):
	
	bot = params['bot']
	invite = params['invite']
	notify_timeout_release = None
	
	# @bot.event
	# async def on_user_update(before, after):
	# 	try:
	# 		guild = bot.get_guild(guildId)
	# 		new_name = after.name
	# 		list_rules = await guild.fetch_automod_rules()
	# 		for rule in list_rules:
	# 			if not (str(rule.event_type) == 'AutoModEventType.message_send'):
	# 				if new_name in rule.trigger_metadata.keyword_filter:
	# 					print('Rule not respected')
	# 				# print(rule.name)
	# 				# print(rule.trigger_metadata.keyword_filter, sep=", ")
	# 				# print('--------------')
	# 	except Exception as ex:
	# 		print('----- on_user_update(evt) -----')
	# 		print(ex)
	# 		await log_exception(ex, 'on_user_update(evt)', None, bot)


	@bot.event
	async def on_member_update(before, after):
		try:
			nonlocal notify_timeout_release
			if (after.id == users['owner']):
				return
			else:
				await check_nickname(before, after)
				await check_timeout(params, before, after, notify_timeout_release)
		except Exception as ex:
			print('----- on_member_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_update(evt)', None, bot)
			raise ex

	######################## JOIN MEMBER ########################
	@bot.event
	async def on_member_join(member):
		try:			
			if member.bot and (os.getenv("kick_bot") == "1"):
				await member.kick(reason=f"Kicked a bot (ID: {member.id})")
				return
			msg = await welcomeMember(params, member, 1, 1, 1, 1)
			channel = bot.get_channel(textChannels['log-server'])
			await channel.send(msg.strip())

			data = await invite.get_invite(member)
			channel = bot.get_channel(textChannels['log-common'])
			inviter = 'None'
			msg = f'<@{member.id}> / {member.id} was invited'
			if hasattr(data, 'inviter') and data.inviter: 
				inviter = f'<@{data.inviter.id}> / {data.inviter.id}'
			msg += f'\n\tInviter : {inviter}'
			if hasattr(data, 'channel'): msg += f'\n\tChannel : <#{data.channel.id}>'
			if hasattr(data, 'id'): msg += f'\n\tId : {data.id}'
			if hasattr(data, 'code'): msg += f'\n\tCode : {data.code}'
			if hasattr(data, 'created_at') and data.created_at:
				created_at = getTimeUtcPlusOne(data.created_at, "%A, %B %d, %Y - %H:%M")
				msg += f'\n\tCreated at : {created_at}'
			expires_at = 'Never'
			if hasattr(data, 'expires_at') and data.expires_at:
				expires_at = getTimeUtcPlusOne(data.expires_at, "%A, %B %d, %Y - %H:%M")
			msg += f'\n\tExpires at : {expires_at}'
			if hasattr(data, 'guild_scheduled_event') and data.guild_scheduled_event:
				msg += f'\n\tEvent : {data.guild_scheduled_event.name}'
			await channel.send(msg)
		
		except Exception as ex:
			print('----- on_member_join(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_join(evt)', None, bot)
		

	######################## REMOVE MEMBER ########################
	@bot.event
	async def on_member_remove(member):
		try:
			if member.bot:
				channel = bot.get_channel(textChannels['log-server'])
				await channel.send(f"🤖 kicked a bot (ID: {member.id})")
			membersCount = await updateMembersCount(params)
			channel = bot.get_channel(textChannels['log-server'])
			isDeletedUser = "🗑️" if "Deleted User" in member.name else ""
			msg = f'🟥 {isDeletedUser} {membersCount} - {member.mention} / {member.name} / {member.id} left'
			msg += '\n──────────────────────'
			await channel.send(msg.strip())
		except Exception as ex:
			print('----- on_member_remove(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_remove(evt)', None, bot)

	######################## WELCOME MEMBER ########################
	