from setup.properties import *
from setup.actions import *

def init_msg_activity(params):
	
	bot = params['bot']

	######################## ON MESSAGE ########################
	@bot.event
	async def on_message(message):
		try:
			if str(message.channel.type) == 'private':
				try:
					await log_member_dms(message)
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
				
			try:
				if await prohibited_mentions(message):
					return
				# if await check_spam(message):
				# 	return
			except Exception as ex:
				print('----- on_message(evt)/everyone|spam -----')
				print(ex)
				await log_exception(ex, 'on_message(evt)/everyone|spam', None, bot)
			
			await bot.process_commands(message)
		except Exception as ex:
			print('----- on_message(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message(evt)', None, bot)

	async def log_member_dms(message):
		author = message.author
		# Testing
		if author.id == users['drissboumlik']:
			channel = author.dm_channel
			await channel.send('am alive')
			return
		excludedIDs = [
				users['drissboumlik'],
				users['teabot'],
			]
		if author.id not in excludedIDs:
			channel = bot.get_channel(textChannels['log-dms'])
			msgs = []
			msg = '──────────────────────'
			msg += f'\nDM/ ◁='
			msg += f'\n__From__\n{author} - {author.mention}'
			msg += f'\n__Content__\n'
			msgs.append(msg) #await channel.send(msg)
			msg_content = f'{"--Sticker--" if (message.content == "") else message.content}'
			msgs.append(msg_content) #await channel.send(msg_content)
			msg = get_attachments(message)
			if msg: msgs.append(msg) #await channel.send(msg)
			msg = get_embeds(message)
			if msg: msgs.append(msg) #await channel.send(msg)
			for msg in msgs:
				await channel.send(msg)

	async def prohibited_mentions(message):
		content = message.content
		if str(message.channel.type) == 'text':
			if content.count('@everyone') or content.count('@here'):
				msg = 'Dont mention __everyone__ or __here__ please\n*Your message will be deleted after 5 seconds !!*'
				await message.channel.send(msg, delete_after = 10)
				await message.delete(delay=10)
				return True
		return False
	
	async def check_spam(message):
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

	######################## ON MESSAGE DELETE ########################
	@bot.event
	async def on_message_delete(message):
		try:
			if str(message.channel.type) == 'private':
				return
			excludedCategories = [
				categories['system-corner']
			]
			if message.channel.category_id in excludedCategories:
				return
				
			log = bot.get_channel(textChannels['log-txt'])
			msgs = []
			msg = '──────────────────────'
			msg += f'\n🗑 by {message.author.mention} in {message.channel.mention}'
			created_at = getTimeUtcPlusOne(message.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if message.edited_at:
				edited_at = getTimeUtcPlusOne(message.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n{created_at} ➜ {edited_at}'
			msg += f'\n__Content__\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = f'{"--Sticker | Empty--" if (message.content == "") else message.content}'
			msgs.append(msg_content) #await log.send(msg_content)
			msg = get_attachments(message)
			if msg: msgs.append(msg) #await log.send(msg)
			msg = get_embeds(message)
			if msg: msgs.append(msg) #await log.send(msg)
			for msg in msgs:
				await log.send(msg)

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
				categories['system-corner']
			]
			if before.channel.category_id in excludedCategories:
				return
			if (before.content.lower() == after.content.lower()):
				return
			log = bot.get_channel(textChannels['log-txt'])
			msgs = []
			msg = f'\n\nhttps://discord.com/channels/{guildId}/{after.channel.id}/{after.id}'
			msg += f'\n✏ by {before.author.mention} in {before.channel.mention}'
			created_at = getTimeUtcPlusOne(after.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if after.edited_at:
				edited_at = getTimeUtcPlusOne(after.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n📅 {created_at} ➜ {edited_at}'
			msg += f'\n__Content__\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = f'{"--Sticker | Empty--" if (before.content == "") else before.content}'
			msgs.append(msg_content) #await log.send(msg_content)
			msg = '\n──▼▼▼▼▼──\n'
			msgs.append(msg) #await log.send(msg)
			msg_content = f'{"--Sticker | Empty--" if (after.content == "") else after.content}'
			msgs.append(msg_content) #await log.send(msg_content)
			msg = get_attachments(before)
			if msg: msgs.append(msg) #await log.send(msg)
			msg = get_embeds(before)
			if msg: msgs.append(msg) #await log.send(msg)
			# msg += '\n──────────────────────'
			# msgs.append(msg) #await log.send(msg)
			for msg in msgs:
				await log.send(msg)
		except Exception as ex:
			print('----- on_message_edit(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message_edit(evt)', None, bot)
