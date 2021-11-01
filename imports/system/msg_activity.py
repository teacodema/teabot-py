from setup.properties import *
from setup.actions import *


def init_msg_activity(params):
	
	bot = params['bot']

	######################## ON MESSAGE ########################
	@bot.event
	async def on_message(message):
		try:
			excludedCategories = [
				categories['system-corner']
			]

			try:
				content = message.content
				if str(message.channel.type) == 'text' and message.channel.category_id not in excludedCategories:
					if content.count('@everyone') or content.count('@here'):
						channel = message.channel
						msg = 'Dont mention __everyone__ or __here__ please\nYour message will be deleted after 5 seconds'
						await channel.send(msg, delete_after = 10)
						await message.delete(delay=10)
						return

					blocked = [
						'dlscord', 'discordnitro', 'discordglfts',
						'discord-airdrop', 'discocrd-nitro'
					]
					spam = False
					for b in blocked:
						if message.content.count(b) > 0:
							print('spam message')
							await message.delete()
							spam = True
					if spam:
						return
			except Exception as ex:
					print('----- on_message 2 -----')
					print(ex)

			if str(message.channel.type) == 'private':
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
				if (author.id not in excludedIDs):
					msg = '──────────────────────'
					msg = f'\nDM/ 🡷'
					msg+= f'\n__From__\n{author} - {author.mention}'
					msg += f'\n__Content__\n{"--Sticker--" if (message.content == "") else message.content}'
					if len(message.attachments):
						attachmentsUrls = '\n__Attachments__\n'
						for attch in message.attachments:
							attachmentsUrls += f'{attch.url}\n'
						msg += attachmentsUrls
					
					if len(message.embeds):
						embedsUrls = '\n__Embeds__\n'
						for attch in message.embeds:
							embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
						msg += embedsUrls

					channel = bot.get_channel(textChannels['log-channel'])
					await channel.send(msg)
			# else:
			# 	author = message.author
			# 	if author.id == users['drissboumlik']:
			# 		print(message.content)
			await bot.process_commands(message)
		except Exception as ex:
			print('----- on_message 1 -----')
			print(ex)


	######################## ON MESSAGE DELETE ########################
	@bot.event
	async def on_message_delete(message):
		try:
			excludedAuthors = [
				# users['drissboumlik']
				# users['teacode'],
				# users['teabot'],
			]
			
			messageAuthorId = message.author.id
			if messageAuthorId not in excludedAuthors:
				msg = '──────────────────────'
				msg += f'\n🗑 by {message.author.mention} in {message.channel.mention}'
				msg += f'\n{message.created_at} ➜ {message.edited_at}'
				msg += f'\n__Content__\n{message.content}'

				if len(message.attachments):
					attachmentsUrls = '\n__Attachments__\n'
					for attch in message.attachments:
						attachmentsUrls += f'{attch.url}\n'
					msg += attachmentsUrls

				if len(message.embeds):
					embedsUrls = '\n__Embeds__\n'
					for attch in message.embeds:
						embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
					msg += embedsUrls

				logChannelActivity = bot.get_channel(textChannels['log-channel'])
				await logChannelActivity.send(msg)
		except Exception as ex:
			print('----- on_message_delete -----')
			print(ex)


	######################## ON MESSAGE EDIT ########################
	@bot.event
	async def on_message_edit(before, after):
		try:
			excludedAuthors = [
				# users['drissboumlik']
				# users['teacode'],
				# users['teabot'],
			]

			if (before.content.lower() == after.content.lower()):
				return

			messageAuthorId = before.author.id
			if messageAuthorId not in excludedAuthors:
				msg = '──────────────────────'
				msg += f'\n✏ by {before.author.mention} in {before.channel.mention}'
				msg += f'\n{after.created_at} ➜ {after.edited_at}'
				msg += f'\n__Content__\n{before.content}\n▼\n{after.content}'

				if len(before.attachments):
					attachmentsUrls = '\n__Attachments__\n'
					for attch in before.attachments:
						attachmentsUrls += f'{attch.url}\n'
					msg += attachmentsUrls

				if len(before.embeds):
					embedsUrls = '\n__Embeds__\n'
					for attch in before.embeds:
						embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
					msg += embedsUrls
					
				logChannelActivity = bot.get_channel(textChannels['log-channel'])
				await logChannelActivity.send(msg)
		except Exception as ex:
			print('----- on_message_edit -----')
			print(ex)
