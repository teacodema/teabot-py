from setup.data.properties import *
from setup.actions.common import *
from setup.actions.member import *

def init_events_member(params):
	
	bot = params['bot']
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
			if member.bot:
				await member.kick(reason=f"Kicked a bot (ID: {member.id})")
				return
			msg = await welcomeMember(params, member, 1, 1, 1)
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
			membersCount = await updateMembersCount(params, member)
			channel = bot.get_channel(textChannels['log-server'])
			_name = replace_str(member.name, {"_": "\_", "*": "\*"})
			_display_name = replace_str(member.display_name, {"_": "\_", "*": "\*"})
			msg = f'🟥 **{membersCount}** - {member.mention} / [{_name}#{member.discriminator}] / ({_display_name}) / ({member.id}) left **TeaCode**'
			await channel.send(msg)
		except Exception as ex:
			print('----- on_member_remove(evt) -----')
			print(ex)
			await log_exception(ex, 'on_member_remove(evt)', None, bot)

	######################## WELCOME MEMBER ########################
	