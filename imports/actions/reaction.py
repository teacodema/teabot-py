from imports.data_server.reactions import *
from imports.data_server.channels_categories import *
from imports.actions.common import *
from imports.actions.message import *


async def log_reacted_msg(params, payload, member, operation="++"):
	bot = params['bot']
	discord = params['discord']
	_ch = bot.get_channel(payload.channel_id)
	if not _ch: _ch = await bot.fetch_channel(payload.channel_id)
	url = get_message_link(payload.channel_id, payload.message_id)
	user_mention = await toggle_user_mention(bot, member, [roles['viewer']])
	if str(_ch.type) == 'private': log = bot.get_channel(textChannels['log-reaction-dms'])
	else: log = bot.get_channel(textChannels['log-reaction'])
	
	log_thread = await make_thread(log, f'{payload.emoji} {operation} {user_mention} in {toggle_channel_mention(_ch)}')
	thread_first_msg = f'{url}\n{user_mention} {operation} {payload.emoji} - ({payload.emoji.id})\nMember ID : {member.id}'
	await log_thread.send(thread_first_msg)
	
	excludedCategories = [
		categories['system-corner'],
		categories['information'],
	]

	if (_ch == None) or (hasattr(_ch, 'category_id') and _ch.category_id in excludedCategories):
		return log_thread

	m = await _ch.fetch_message(payload.message_id)
	if m:
		msgs = []
		user_mention = await toggle_user_mention(bot, m.author, [roles['viewer']])
		msg = f'\nMessage ID : {m.id}'
		msg += f'\nChannel ID : {m.channel.id}'
		msg += f'\n✉ by {user_mention} in {toggle_channel_mention(m.channel)}'
		msg += f'\nAuthor ID : {m.author.id}'
		created_at = getTimeUtcPlusOne(m.created_at, "%d %B %Y - %H:%M")
		edited_at = None
		if m.edited_at:
			edited_at = getTimeUtcPlusOne(m.edited_at, "%d %B %Y - %H:%M")
		msg += f'\n📅 {created_at} ➜ {edited_at}'
		msg += f'\n__Content__\n'
		msgs.append(msg) # await log.send(f'{msg}')
		msg_content = get_message_content(m)
		msgs.append(msg_content) # await log.send(f'{msg_content}')
		attachments_data = get_attachments(m, discord)
		if attachments_data['urls']: msgs.append(attachments_data['urls']) #await log.send(msg)
		msg = get_embeds(m)
		if msg: msgs.append(msg) #await log.send(msg)
		# msg = f'\n──────────────────────'
		# await log.send(f'{msg}')
		for msg in msgs:
			await log_thread.send(msg.strip())
		if attachments_data['files']: await log_thread.send(files = attachments_data['files'])
	return log_thread
	# await log_thread.edit(archived=True)

