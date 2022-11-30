from setup.data.params import * 
from setup.data.properties import *
from setup.actions.common import *
from setup.actions.message import *


async def log_reacted_msg(params, payload, log, member, adding=True):
	bot = params['bot']
	_ch = bot.get_channel(payload.channel_id)
	url = f'https://discord.com/channels/{guildId}/{payload.channel_id}/{payload.message_id}'
	operation = f'{"🔹 Added" if adding else "🔸 Removed"}'
	user_mention = toggle_user_mention(bot, member, roles['mods'])
	log_thread = await make_thread(log, f'Reaction {operation} by {user_mention} in {toggle_channel_mention(_ch)}')
	thread_first_msg = f'{url}\n{user_mention} {operation} {payload.emoji} - ({payload.emoji.id})\nMember ID : {member.id}'
	await log_thread.send(thread_first_msg)
	
	excludedCategories = [
		categories['system-corner'],
		categories['information'],
	]
	if not _ch:
		_ch = await bot.fetch_channel(payload.channel_id)

	if (_ch == None) or (hasattr(_ch, 'category_id') and _ch.category_id in excludedCategories):
		return log_thread

	m = await _ch.fetch_message(payload.message_id)
	if m:
		msgs = []
		user_mention = toggle_user_mention(bot, m.author, roles['mods'])
		msg = f'\n✉ by {user_mention} in {toggle_channel_mention(m.channel)}'
		msg += f'\nAuthor ID : {m.author.id}'
		created_at = getTimeUtcPlusOne(m.created_at, "%d %B %Y - %H:%M")
		edited_at = None
		if m.edited_at:
			edited_at = getTimeUtcPlusOne(m.edited_at, "%d %B %Y - %H:%M")
		msg += f'\n📅 {created_at} ➜ {edited_at}'
		msg += f'\n__Content__\n'
		msgs.append(msg) # await log.send(f'{msg}')
		msg_content = f'{"--Sticker | Empty--" if (m.content == "") else m.content}'
		msgs.append(msg_content) # await log.send(f'{msg_content}')
		# msg = get_attachments(m)
		# if msg: msgs.append(msg) #await log.send(msg)
		# msg = get_embeds(m)
		# if msg: msgs.append(msg) #await log.send(msg)
		# msg = f'\n──────────────────────'
		# await log.send(f'{msg}')
		for msg in msgs:
			await log_thread.send(msg)
	return log_thread
	# await log_thread.edit(archived=True)


async def update_msg_reactions(params, guild, channel, msg_id):
	try:
		discord = params['discord']
		msg = await channel.fetch_message(int(msg_id))
		roles_assigned = 0
		_msg = ''
		for r in msg.reactions:
			roleName = reactions[str(channel.id)][str(msg_id)][str(r.emoji)]
			role = discord.utils.get(guild.roles, name = roleName)
			reacted_users = await r.users().flatten()
			for u in reacted_users:
				try:
					if u.id != users['teabot']:
						member = await guild.fetch_member(u.id)
						if role not in member.roles:
							await member.add_roles(role)
							_msg += f'{member.display_name}#{member.discriminator} got {role.mention}\n'
							_msg += f'Member ID : {member.id} / {member.mention}\n'
							roles_assigned += 1
				except Exception as ex:
					print('---------- /update_msg_reactions()/add role user --------')
					print(ex)
					print(role.name)
					print(u.name)
					await msg.remove_reaction(r.emoji, u)
					pass
		return {'roles_assigned': roles_assigned, '_msg': _msg}
	except Exception as ex:
		print('---------- /update_msg_reactions()/msg reactions --------')
		print(ex)
		print(channel.name)
		print(role.name)
		pass