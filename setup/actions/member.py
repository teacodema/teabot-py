from datetime import datetime
from setup.data.properties import *
from setup.data.params import *
from setup.actions.common import *
from setup.actions.role import *

async def checkNewMemberRole(guild, do:int=0):
	try:
		role = guild.get_role(roles['new-members'])
		updated = []
		for member in role.members:
			diff = datetime.now() - member.joined_at.replace(tzinfo=None)
			if diff.days >= appParams['newMembershipPeriode']:
				updated.append(member.mention)
				if do: await member.remove_roles(role)
		return updated
	except Exception as ex:
		print('----- checkNewMemberRole -----')
		print(ex)
		return -1

async def welcomeMember(params, member, assign_role = 0, send_dm = 0, use_webhook = 0):
	try:
		bot = params['bot']
		channel = bot.get_channel(textChannels['log-server'])
		msg = '──────────────────────'
		if int(use_webhook):
			wh_made = await make_webhook(params, member, channel)
			if wh_made: msg += '\n✅ Webhook made'
			else: msg += '\n❌ Webhook not made' 
		if int(assign_role):
			assigned = await assign_init_roles(params, member)
			if assigned: msg += "\n🟢 initial roles assigned 🎭"
			else: msg += "\n🔴 initial roles assigned 🎭"
		if int(send_dm):
			dm_sent = await send_dm_welcome(params, member)
			if dm_sent: msg +=f'\n📨 DM/ Welcome Message ➜ **{member.name}#{member.discriminator}** / Member ID : {member.id}'
			else: msg += f'\n❗ DM/ Welcome Message ➜ **{member.name}#{member.discriminator}** / Member ID : {member.id}'
		membersCount = await updateMembersCount(params)
		_name = replace_str(member.name, {"_": "\_", "*": "\*"})
		_display_name = replace_str(member.display_name, {"_": "\_", "*": "\*"})
		msg += f'\n🟩 **{membersCount}** - {member.mention} / [{_name}#{member.discriminator}] / ({_display_name}) / ({member.id}) join **TeaCode**'
		return msg
	except Exception as ex:
		print('----- welcomeMember() -----')
		print(ex)
		await log_exception(ex, 'welcomeMember()', None, bot)
		return 0

async def send_dm_welcome(params, member):
	try:
		bot = params['bot']
		startHereChannel = bot.get_channel(textChannels['start-here'])
		invite = await startHereChannel.create_invite(max_age=appParams['inviteMaxAge'], max_uses=appParams['inviteMaxUses'], reason=f'Welcoming member (ID: {member.id})')
		message = f"📌 *This is an automated welcoming message (No need to reply)* ‼"
		message += f'\n\nMerhba bik m3ana {member.mention} f **TeaCode** Community  :flag_ma:  👋'

		message += f"\n\nHna ghadi tl9a chno tehtaj bach takhod fikra 3la server ➜ <#{textChannels['start-here']}>"
		message += f"\nSowwel hna ➜ <#{textChannels['ask-staff']}> ila htajiti chi haja f server."
		message += f"\nDon't forget to **invite** your friends who could be interested (Link : {invite})"
		message += f"\n\n➜ Ila ma3reftich chno dir t9der tsowwel <@{users['drissboumlik']}>"
		message += f"\n➜ Website : <https://teacode.ma>"

		channel = await member.create_dm()
		await channel.send(message)
		return 1
	except Exception as ex:
		print('----- send_dm_welcome() -----')
		print(ex)
		await log_exception(ex, 'send_dm_welcome()', None, bot)
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
		memberList = guild.members
		membersCount = len(memberList)
		return membersCount
	except Exception as ex:
		print('----- updateMembersCount() -----')
		print(ex)
		await log_exception(ex, 'updateMembersCount()', None, bot)

async def assign_init_roles(params, member):
	try:
		bot = params['bot']
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

async def check_timeout(params, before, after, notify_timeout_release):
	bot = params['bot']
	tasks = params['tasks']
	if before.current_timeout != after.current_timeout:
		channel = bot.get_channel(textChannels['log-server'])
		if after.current_timeout:
			msg = f"⏱🔴 {after.mention} is timedout & will be untimedout on {getTimeUtcPlusOne(after.current_timeout)}"
			if notify_timeout_release:
				end_task(notify_timeout_release)
			@tasks.loop(time=after.current_timeout.time(), reconnect=True)
			async def notify_timeout_release():
				await channel.send(f"⏱🟢 {after.mention} is released from timeout")
			start_task(notify_timeout_release)
		else:
			msg = f"⏱🟢 {after.mention} is released from timeout"
		await channel.send(msg)