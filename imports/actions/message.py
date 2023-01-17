from datetime import datetime
from imports.data.properties import *
from imports.actions.common import *

def get_message_content(msg):
	return f'{"--Sticker | Empty--" if (msg.content == "") else msg.content}'

async def make_thread(channel, headerMsg, threadName=None):
	threadMsg = await channel.send(headerMsg)
	log_thread = await threadMsg.create_thread(name=threadName or headerMsg)
	return log_thread

def toggle_channel_mention(channel, mention = True):
	if str(channel.type) == 'private':
		return channel.id
	if mention == False: 
		return channel.name
	return f'<#{channel.id}>'

async def toggle_user_mention(bot, _member, roleId, append_member_id = False):
	guild = bot.get_guild(guildId)
	member = guild.get_member(_member.id)
	if member == None:
		member = await bot.fetch_user(_member.id)
	user_mention = member.mention
	role = guild.get_role(roleId)
	if (not role) or (hasattr(member, 'roles') and role in member.roles):
		user_mention = f'{member.display_name}#{member.discriminator}'
	if append_member_id: user_mention += f' / {member.id}'
	return user_mention

def get_attachments(message):
	if len(message.attachments):
		attachmentsUrls = '\n__Attachments__\n'
		for attch in message.attachments:
			attachmentsUrls += f'{attch.url}\n'
		return attachmentsUrls
	return ''

def get_embeds(message):
	if len(message.embeds):
		embedsUrls = '\n__Embeds__\n'
		for embed in message.embeds:
			embedsUrls += f'{embed.url} - {embed.image} - {embed.author.mention} - {embed.description}\n'
			for field in embed.fields:
				embedsUrls += f'\t- {field.name} (field name) : {field.value} (field value)\n'
		return embedsUrls
	return ''


async def log_member_dms(params, message):
	bot = params['bot']
	author = message.author
	# Testing
	if author.id == users['drissboumlik']:
		channel = await author.create_dm()
		await channel.send('am alive')
		return
	excludedIDs = [
			users['drissboumlik'],
			users['teabot'],
		]
	if author.id not in excludedIDs:
		channel = bot.get_channel(textChannels['log-dms'])
		user_mention = await toggle_user_mention(bot, author, roles['root'], True)
		log_thread = await make_thread(channel, f'✉ DM/ ◁== {user_mention}')
			
		msgs = []
		msg = f'\n__From__\n{user_mention}'
		msg += f'\n__Content__\n'
		msgs.append(msg) #await channel.send(msg)
		msg_content = f'{"--Sticker--" if (message.content == "") else message.content}'
		msgs.append(msg_content) #await channel.send(msg_content)
		msg = get_attachments(message)
		if msg: msgs.append(msg) #await channel.send(msg)
		msg = get_embeds(message)
		if msg: msgs.append(msg) #await channel.send(msg)
		for msg in msgs:
			await log_thread.send(msg.strip())
		await log_thread.edit(archived=True)

async def prohibited_mentions(message):
	content = message.content
	channel_type = str(message.channel.type)
	if channel_type == 'text' or channel_type == 'public_thread':
		if content.count('@everyone') or content.count('@here'):
			msg = 'Dont mention __everyone__ or __here__ please\n*Your message will be deleted after 5 seconds !!*'
			await message.channel.send(msg.strip(), delete_after = 10)
			await message.delete(delay=10)
			return True
	return False

async def check_spam(params, message):
	bot = params['bot']
	blocked = [
		'dlscord', 'discordnitro', 'discordglfts',
		'discord-airdrop', 'discocrd-nitro', 'discode'
	]
	spam = False
	channel = bot.get_channel(textChannels['log-txt'])
	for b in blocked:
		if message.content.count(b) > 0:
			_msg = '──────────────────────'
			_msg = f'\nspam message from {message.author.mention} on {message.channel.mention}'
			await channel.send(_msg)
			await message.delete()
			spam = True
	return spam


async def send_dm_msg(interaction, message, member):
	try:
		channel = member.dm_channel
		if channel == None:
			channel = await member.create_dm()
		return await channel.send(message)
	except Exception as ex:
		print('----- send_dm_msg() -----')
		print(ex)
		msg = f'Cannot send messages to {member.mention} / {member.name}#{member.discriminator}'
		await log_exception(ex, 'send_dm_msg()', interaction, None, True, msg)
		return None

def isNotPinned(msg):
	return not msg.pinned

async def deleteMsg(params, interaction, limit):
	try:
		deletedMsgs = []
		deletedMsgs = await interaction.channel.purge(limit = limit, check = isNotPinned, bulk = True)
		if (len(deletedMsgs) > 0):
			return list(set(deletedMsgs + await deleteMsg(params, interaction, limit)))
		else:
			return []
	except Exception as ex:
		print('----- deleteMsg() -----')
		print(ex)
		await log_exception(ex, 'deleteMsg()', interaction)
		return deletedMsgs

async def logPurgedMessages(params, interaction, count, _purgedMsgs):
	bot = params['bot']
	log = bot.get_channel(textChannels['log-msg'])
	dt = replace_str(getTimeUtcPlusOne(datetime.now()), {":": "."})
	headerMsg = f"🗑 **purge({count})** | {interaction.channel.mention}"
	headerMsg += f"\n__Date__ : {dt}"
	log_thread = await make_thread(log, headerMsg, f"{interaction.channel.name} | {dt}")

	msgIndex = 1
	for m in _purgedMsgs:
		msg = f'───────────\t**{msgIndex}**\t───────────'
		msg += f'\n🗑 by {m.author.display_name}#{m.author.discriminator} in {m.channel.mention}'
		msg += f'\nAuthor ID : {m.author.id}'
		created_at = getTimeUtcPlusOne(m.created_at, "%d %B %Y - %H:%M")
		edited_at = None
		if m.edited_at:
			edited_at = getTimeUtcPlusOne(m.edited_at, "%d %B %Y - %H:%M")
		msg += f'\n📅 {created_at} ➜ {edited_at}'
		msg += "\n__Content__\n"
		msg_content = get_message_content(m)
		if len(msg_content) >= 1800: 
			await log_thread.send(msg.strip())
			await log_thread.send(msg_content.strip())
			msg = ''
		else:
			msg += f'{msg_content}'
		msg += get_attachments(m)
		msg += get_embeds(m)
		await log_thread.send(msg.strip())
		msgIndex += 1
	await log_thread.edit(archived=True)
