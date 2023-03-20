from imports.data_server.config import *
from imports.actions.message import *
from imports.actions.common import *

def init_events_message(params):
	
	bot = params['bot']

	######################## ON MESSAGE ########################
	@bot.event
	async def on_message(message):
		try:
			if str(message.channel.type) == 'private':
				try:
					await log_member_dms(params, message)
				except Exception as ex:
					print('----- on_message(evt)/log_dms -----')
					print(ex)
					await log_exception(ex, 'on_message(evt)/log_dms', None, bot)
				return
			excludedCategories = [
				categories['system-corner']
			]
			if message.channel.category_id in excludedCategories:
				return
				
			# try:
			# 	if await prohibited_mentions(message):
			# 		return
			# 	# if await check_spam(message):
			# 	# 	return
			# except Exception as ex:
			# 	print('----- on_message(evt)/everyone|spam -----')
			# 	print(ex)
			# 	await log_exception(ex, 'on_message(evt)/everyone|spam', None, bot)
			
			# await bot.process_commands(message)
		except Exception as ex:
			print('----- on_message(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message(evt)', None, bot)

	######################## ON MESSAGE DELETE ########################
	@bot.event
	async def on_message_delete(message):
		try:
			if str(message.channel.type) == 'private':
				return
			excludedCategories = [
				categories['system-corner'],
			]
			if message.channel.category_id in excludedCategories:
				return
				
			log = bot.get_channel(textChannels['log-txt'])
			user_mention = await toggle_user_mention(bot, message.author, [roles['viewer']])
			log_thread = await make_thread(log, f'🗑 {user_mention} in {toggle_channel_mention(message.channel)}')
			
			msgs = []
			msg = '──────────────────────'
			msg += f'\n🗑 {user_mention} in {message.channel.mention}'
			msg += f'\nAuthor ID : {message.author.id}'
			created_at = getTimeUtcPlusOne(message.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if message.edited_at:
				edited_at = getTimeUtcPlusOne(message.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n📅 {created_at} ➜ {edited_at}'
			msg += f'\n__Content__\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = get_message_content(message)
			msgs.append(msg_content) #await log.send(msg_content)
			msg = get_attachments(message)
			if msg: msgs.append(msg) #await log.send(msg)
			msg = get_embeds(message)
			if msg: msgs.append(msg) #await log.send(msg)
			for msg in msgs:
				await log_thread.send(msg.strip())
			await log_thread.edit(archived=True)

		except Exception as ex:
			print('----- on_message_delete(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message_delete(evt)', None, bot)


	######################## ON MESSAGE EDIT ########################
	@bot.event
	async def on_message_edit(before, after):
		try:
			if str(before.channel.type) == 'private':
				return
			excludedCategories = [
				categories['system-corner'],
			]
			if before.channel.category_id in excludedCategories:
				return
			if (before.content.lower() == after.content.lower()):
				return
			log = bot.get_channel(textChannels['log-txt'])
			user_mention = await toggle_user_mention(bot, before.author, [roles['viewer']])
			log_thread = await make_thread(log, f'✏ {user_mention} in {toggle_channel_mention(before.channel)}')
			
			msgs = []
			msg = f'\n\nhttps://discord.com/channels/{guildId}/{after.channel.id}/{after.id}'
			user_mention = await toggle_user_mention(bot, before.author, [roles['viewer']])
			msg += f'\n✏ {user_mention} in {before.channel.mention}'
			msg += f'\nAuthor ID : {before.author.id}'
			created_at = getTimeUtcPlusOne(after.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if after.edited_at:
				edited_at = getTimeUtcPlusOne(after.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n📅 {created_at} ➜ {edited_at}'
			msg += f'\n__Content__\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = get_message_content(before)
			msgs.append(msg_content) #await log.send(msg_content)
			msg = '\n──▼▼▼▼▼──\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = get_message_content(after)
			msgs.append(msg_content) #await log.send(msg_content)
			msg = get_attachments(before)
			if msg: msgs.append(msg) #await log.send(msg)
			msg = get_embeds(before)
			if msg: msgs.append(msg) #await log.send(msg)
			# msg += '\n──────────────────────'
			# msgs.append(msg) #await log.send(msg)
			for msg in msgs:
				await log_thread.send(msg.strip())
			await log_thread.edit(archived=True)
		except Exception as ex:
			print('----- on_message_edit(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message_edit(evt)', None, bot)
