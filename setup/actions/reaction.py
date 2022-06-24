from setup.data.properties import *
from setup.actions.common import *


async def log_reacted_msg(params, payload, log, member, adding=True):
	bot = params['bot']
	url = f'https://discord.com/channels/{guildId}/{payload.channel_id}/{payload.message_id}'
	operation = f'{"Added" if adding else "Removed"}'
	await log.send(f'{url}\n{member.mention} {operation} {payload.emoji} - ({payload.emoji.id})')

	_ch = bot.get_channel(payload.channel_id)

	if _ch.category_id == categories['information']:
		return

	m = await _ch.fetch_message(payload.message_id)
	if m:
		msgs = []
		msg = f'\n✉ by {m.author.display_name} in {m.channel.mention}'
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
			await log.send(msg)

