import os
from imports.data.properties import *
from imports.actions.common import *
from imports.actions.member import *

def init_events_member(params):
	
	bot = params['bot']
	invite = params['invite']
	notify_timeout_release = None
	

	@bot.event
	async def on_member_update(before, after):
		try:
			nonlocal notify_timeout_release
			if (after.id == users['drissboumlik']):
				return
			else:
				await check_nickname(before, after)
				await check_timeout(params, before, after, notify_timeout_release)
		except Exception as ex:
			print('----- on_member_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_update(evt)', None, bot)

	######################## JOIN MEMBER ########################
	@bot.event
	async def on_member_join(member):
		try:			
			# print(data.inviter)
			if member.bot and (os.getenv("kick_bot") == "1"):
				await member.kick(reason=f"Kicked a bot (ID: {member.id})")
				return
			msg = await welcomeMember(params, member, 1, 1, 1)
			channel = bot.get_channel(textChannels['log-server'])
			await channel.send(msg.strip())

			data = await invite.get_invite(member)
			channel = bot.get_channel(textChannels['log-common'])
			inviter = 'None'
			msg = f'<@{member.id}>/{member.id} was invited'
			if hasattr(data, 'inviter') and data.inviter: 
				inviter = f'<@{data.inviter.id}> / {data.inviter.id}'
			msg += f'\n\tInviter : {inviter}'
			if hasattr(data, 'channel'): msg += f'\n\tChannel : <#{data.channel.id}>'
			if hasattr(data, 'id'): msg += f'\n\tId : {data.id}'
			if hasattr(data, 'code'): msg += f'\n\tCode : {data.code}'
			if hasattr(data, 'created_at'):
				created_at = getTimeUtcPlusOne(data.created_at, "%A, %B %d, %Y - %H:%M")
				msg += f'\n\tCreated at : {created_at}'
			expires_at = 'Never'
			if data.expires_at: 
				expires_at = getTimeUtcPlusOne(data.expires_at, "%A, %B %d, %Y - %H:%M")
			msg += f'\n\tExpires at : {expires_at}'
			if hasattr(data, 'guild_scheduled_event') and data.guild_scheduled_event:
				msg += f'\n\tEvent : {data.guild_scheduled_event.name}'
			await channel.send(msg)
		
		except Exception as ex:
			raise ex
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
			membersCount = await updateMembersCount(params)
			channel = bot.get_channel(textChannels['log-server'])
			_name = replace_str(member.name, {"_": "\_", "*": "\*"})
			_display_name = replace_str(member.display_name, {"_": "\_", "*": "\*"})
			msg = f'🟥 **{membersCount}** - {member.mention} / [{_name}#{member.discriminator}] / ({_display_name}) / ({member.id}) left **TeaCode**'
			msg += '\n──────────────────────'
			await channel.send(msg.strip())
		except Exception as ex:
			print('----- on_member_remove(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_remove(evt)', None, bot)

	######################## WELCOME MEMBER ########################
	