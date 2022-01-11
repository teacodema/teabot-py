from setup.properties import *
from setup.actions import *
import pytz

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
			if message.channel.category_id not in excludedCategories:
				try:
					if await prohibited_mentions(message):
						return
					if await check_spam(message):
						return
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
			channel = bot.get_channel(textChannels['log-channel'])
			msg = '──────────────────────'
			msg += f'\nDM/ ◁='
			msg += f'\n__From__\n{author} - {author.mention}'
			msg += f'\n__Content__\n'
			await channel.send(msg)
			msg = f'{"--Sticker--" if (message.content == "") else message.content}'
			await channel.send(msg)
			msg = get_attachments(message)
			if msg: await channel.send(msg)
			msg = get_embeds(message)
			if msg: await channel.send(msg)

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
			'discord-airdrop', 'discocrd-nitro'
		]
		spam = False
		channel = bot.get_channel(textChannels['log-channel'])
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
			if message.channel.category_id not in excludedCategories:
				logChannelActivity = bot.get_channel(textChannels['log-channel'])
				msg = '──────────────────────'
				msg += f'\n🗑 by {message.author.mention} in {message.channel.mention}'
				timeZ_Ma = pytz.timezone('Africa/Casablanca')
				created_at = message.created_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
				edited_at = None
				if message.edited_at:
					edited_at =  message.edited_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
				msg += f'\n{created_at} ➜ {edited_at}'
				msg += f'\n__Content__\n'
				await logChannelActivity.send(msg)
				await logChannelActivity.send(message.content)
				msg = get_attachments(message)
				if msg: await logChannelActivity.send(msg)
				msg = get_embeds(message)
				if msg: await logChannelActivity.send(msg)

		except Exception as ex:
			print('----- on_message_delete(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message_delete(evt)', None, bot)


	######################## ON MESSAGE EDIT ########################
	@bot.event
	async def on_message_edit(before, after):
		try:
			excludedCategories = [
				categories['system-corner']
			]

			if before.channel.category_id not in excludedCategories:
				if (before.content.lower() == after.content.lower()):
					return
				logChannelActivity = bot.get_channel(textChannels['log-channel'])
				msg = '──────────────────────'
				msg += f'\n✏ by {before.author.mention} in {before.channel.mention}'
				
				timeZ_Ma = pytz.timezone('Africa/Casablanca')
				created_at = after.created_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
				edited_at = None
				if after.edited_at:
					edited_at =  after.edited_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
				msg += f'\n{created_at} ➜ {edited_at}'
				msg += f'\n__Content__\n'
				await logChannelActivity.send(msg)
				await logChannelActivity.send(before.content)
				msg = '\n──▼▼▼▼▼──\n'
				await logChannelActivity.send(msg)
				await logChannelActivity.send(after.content)
				msg = get_attachments(before)
				if msg: await logChannelActivity.send(msg)
				msg = get_embeds(before)
				if msg: await logChannelActivity.send(msg)
				msg = f'\n\nhttps://discord.com/channels/{guildId}/{after.channel.id}/{after.id}'
				msg += '\n──────────────────────'
				await logChannelActivity.send(msg)
		except Exception as ex:
			print('----- on_message_edit(evt) -----')
			print(ex)
			await log_exception(ex, 'on_message_edit(evt)', None, bot)
