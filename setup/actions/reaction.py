from setup.data.properties import *
from setup.actions.common import *
from setup.actions.message import *


async def log_reacted_msg(params, payload, log, member, adding=True):
	bot = params['bot']
	url = f'https://discord.com/channels/{guildId}/{payload.channel_id}/{payload.message_id}'
	operation = f'{"🔼 Added" if adding else "🔽 Removed"}'
	user_mention = toggle_mention(member, roles['mods'])
	log_thread = await make_thread(log, f'Reaction {operation}')
	thread_first_msg = f'{url}\n{user_mention} {operation} {payload.emoji} - ({payload.emoji.id})\nMember ID : {member.id}'
	await log_thread.send(thread_first_msg)
	
	excludedCategories = [
		categories['system-corner'],
		categories['information'],
	]
	_ch = bot.get_channel(payload.channel_id)
	if not _ch:
		_ch = await bot.fetch_channel(payload.channel_id)

	if (_ch == None) or (hasattr(_ch, 'category_id') and _ch.category_id in excludedCategories):
		return log_thread

	m = await _ch.fetch_message(payload.message_id)
	if m:
		msgs = []
		user_mention = toggle_mention(m.author, roles['mods'])
		msg = f'\n✉ by {user_mention} in {channel_mention(m.channel)}'
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

