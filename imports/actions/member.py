from datetime import datetime, timedelta, timezone
from imports.data_server.config import *
from imports.data_common.config import *
from imports.actions.common import *
from imports.actions.role import *


async def welcomeMember(params, member, assign_role = 0, send_dm = 0, append_event_to_dm = 0, use_webhook = 0):
	try:
		bot = params['bot']
		channel = bot.get_channel(textChannels['log-server'])
		msg = ''
		if int(use_webhook):
			wh_made = await make_webhook(params, member, channel)
			if wh_made: msg += '\n✅ Webhook made'
			else: msg += '\n❌ Webhook not made' 
		if int(assign_role):
			assigned = await assign_init_roles(params, member)
			if assigned: msg += "\n🟢 initial roles assigned 🎭"
			else: msg += "\n🔴 initial roles assigned 🎭"
		if int(send_dm):
			dm_sent = await send_dm_welcome(params, member, append_event_to_dm)
			if dm_sent: 
				msg +=f'\n📨 DM/ Welcome Message ➜ {member.id}'
				if dm_sent == 2: msg +=f'\n📅 DM/ Next event Notification'
			else: msg += f'\n❗ DM/ Welcome Message ➜ {member.id}'
		membersCount = await updateMembersCount(params)
		msg += f'\n🟩 {membersCount} - {member.mention} / {member.id} join'
		msg += '\n──────────────────────'
		return msg
	except Exception as ex:
		print('----- welcomeMember() -----')
		print(ex)
		await log_exception(ex, 'welcomeMember()', None, bot)
		return 0

async def send_dm_welcome(params, member, append_event_to_dm = 0):
	try:
		returned_value = 1
		bot = params['bot']
		startHereChannel = bot.get_channel(textChannels['start-here'])
		invite = await startHereChannel.create_invite(max_age=appParams['inviteForOneWeek'], max_uses=appParams['inviteMaxUses'], reason=f'Welcoming member (ID: {member.id})')
		message = f"📌 *This is an automated welcoming message (No need to reply)* ‼"
		message += f'\n\nMerhba bik m3ana {member.mention} f **TeaCode** Community  :flag_ma:  👋'

		message += f"\n\nHna ghadi tl9a chno tehtaj bach takhod fikra 3la server ➜ <#{textChannels['start-here']}>"
		message += f"\nSowwel hna ➜ <#{textChannels['ask-staff']}> ila htajiti chi haja f server."
		message += f"\nDon't forget to **invite** your friends who could be interested / Link : {invite}"
		message += f"\n\n➜ Ila ma3reftich chno dir t9der tsowwel <@{users['drissboumlik']}>"
		message += f"\n➜ Website : <https://community.drissboumlik.com>"
		
		if int(append_event_to_dm):
			tzinfo = timezone(timedelta(hours=1))
			now = datetime.now().replace(tzinfo=tzinfo, hour=0, minute=0, second=0, microsecond=0)
			next_week = (now + timedelta(days=8)).replace(tzinfo=tzinfo)
			guild = bot.get_guild(guildId)
			events = sorted(guild.scheduled_events, key=lambda event: event.scheduled_start_time)
			events = list(filter(lambda event: (now < event.scheduled_start_time.replace(tzinfo=tzinfo) and event.scheduled_start_time.replace(tzinfo=tzinfo) < next_week), events))
			if len(events):
				event = events[0]
				invite = await event.channel.create_invite(max_age=appParams['inviteForOneDay'], max_uses=100, reason=f'Invite member to next event : {event.name}')
				event_url = f'{invite}?event={event.id}'
				message += f"\n\n🗓️ Don't forget to join our next event : **{event.name}**\n{event_url}"
				returned_value = 2

		channel = await member.create_dm()
		await channel.send(message)
		return returned_value
	except Exception as ex:
		print('----- send_dm_welcome() -----')
		print(ex)
		# await log_exception(ex, 'send_dm_welcome()', None, bot)
		return 0
			
async def make_webhook(params, member, channel):
	try:
		bot = params['bot']
		webhook = await channel.create_webhook(name=member.name)
		await webhook.send(f'Hi I\'m {member.display_name}/{member.mention}', username=member.name, avatar_url=member.display_avatar.url)
		await webhook.delete()
		return 1
	except Exception as ex:
		print('----- make_webhook() -----')
		print(ex)
		await log_exception(ex, 'make_webhook()', None, bot)
		return 0

######################## UPDATE MEMBERS COUNT ########################
async def updateMembersCount(params):
	try:
		bot = params['bot']
		guild = bot.get_guild(guildId)
		return len(guild.members)
	except Exception as ex:
		print('----- updateMembersCount() -----')
		print(ex)
		await log_exception(ex, 'updateMembersCount()', None, bot)

async def assign_init_roles(params, member):
	try:
		bot = params['bot']
		_roles = [
			roles['members'],
		]
		roles_list = []
		guild = bot.get_guild(guildId)
		for role_id in _roles:	
			role = guild.get_role(role_id)
			roles_list.append(role)
		# await member.add_roles(*roles_list)
		await toggleRole(member, roles_list, True)
		return 1
	except Exception as ex:
		print('----- assign_init_roles() -----')
		print(ex)
		await log_exception(ex, 'assign_init_roles()', None, bot)
		return 0

async def check_nickname(before, after):
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
def getTimeUtcPlusOne(dt, format = "%d %B %Y - %H:%M"):
	timeZ_Ma = pytz.timezone('Africa/Casablanca')
	dt_Ma = dt.astimezone(timeZ_Ma).strftime(format)
	return dt_Ma

async def check_timeout(params, before, after, notify_timeout_release):
	bot = params['bot']
	tasks = params['tasks']
	if before.current_timeout != after.current_timeout:
		channel = bot.get_channel(textChannels['log-server'])
		if after.current_timeout:
			timeoutEndTime = getTimeUtcPlusOne(after.current_timeout, "%d %B %Y - %H:%M")
			msg = f'⏱🔴 {after.mention} is timedout & will be untimedout on {timeoutEndTime}'
			if notify_timeout_release:
				end_task(notify_timeout_release)
			@tasks.loop(time=after.current_timeout.time(), reconnect=False)
			async def notify_timeout_release():
				await channel.send(f"⏱🟢 {after.mention} is released from timeout")
			start_task(notify_timeout_release)
		else:
			msg = f"⏱🟢 {after.mention} is released from timeout"
		await channel.send(msg.strip())