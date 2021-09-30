from setup.properties import *
from setup.actions import *


def init_msg_log(params):
	
	client = params['client']
	

	@client.event
	async def on_message(message):
		try:
			blocked = [
				'dlscordnitro.info', 'discordnitro.info', 'dlscord-nitro.link', 'discord-airdrop.com'
			]
			excludedCategories = [
				categories['system-corner']
			]
			for b in blocked:
				if (message.content.count(b) > 0 and message.channel.category_id not in excludedCategories):
					print('spam message')
					await message.delete()
					return

			if (str(message.channel.type) == 'private'):

				author = message.author
				
				# Testing
				if author.id == users['drissboumlik']:
					channel = author.dm_channel
					await channel.send('am alive')

				excludedIDs = [
						users['drissboumlik'],
						users['teabot'],
						users['teabottest'],
					]
				if (author.id not in excludedIDs):
					attachmentsUrls = ''
					for attch in message.attachments:
						attachmentsUrls += f'{attch.url}\n'			
					channel = client.get_channel(textChannels['log-channel'])
					msgContent = "--Sticker--" if (message.content == "") else message.content
					msgContent += attachmentsUrls
					await channel.send(f'DM/ {author} - {author.mention} : {msgContent}')
		except Exception as ex:
			print('----- on_message -----')
			print(ex)


	
	@client.event
	async def on_message_delete(message):
		try:
			await logDeletedMessage(message, client)
		except Exception as ex:
			print('----- on_message_delete -----')
			print(ex)



	@client.event
	async def on_message_edit(before, after):
		try:
			await logEditedMessage(before, after, client)
		except Exception as ex:
			print('----- on_message_edit -----')
			print(ex)


	######################## LOG MESSAGE ########################
	async def logDeletedMessage(message, client):
		try:
			excludedAuthors = [
				# users['drissboumlik']
				# users['teacode'],
				# users['cartouche'],
				users['teabot'],
				users['YAGPDB'],
			]
			logChannelActivity = client.get_channel(textChannels['log-channel'])

			attachmentsUrls = ''
			for attch in message.attachments:
				attachmentsUrls += f'{attch.url}\n'

			messageAuthorId = message.author.id
			if messageAuthorId not in excludedAuthors:
				msg = f'💢 by {message.author.mention} in {message.channel.mention}'
				msg += f'\n📅 {message.created_at} ➡ {message.edited_at}'
				msg += f'\n"*{message.content}*"'
				msg += attachmentsUrls
				await logChannelActivity.send(msg)
		except Exception as ex:
			print('----- logDeletedMessage -----')
			print(ex)


	async def logEditedMessage(before, after, client):
		try:
			excludedAuthors = [
				# users['drissboumlik']
				# users['teacode'],
				# users['cartouche'],
				users['teabot'],
				users['YAGPDB'],
			]
			logChannelActivity = client.get_channel(textChannels['log-channel'])

			if (before.content.lower() == after.content.lower()):
				return

			attachmentsUrls = ''
			for attch in before.attachments:
				attachmentsUrls += f'{attch.url}\n'

			messageAuthorId = before.author.id
			if messageAuthorId not in excludedAuthors:
				msg = f'✏ by {before.author.mention} in {before.channel.mention}'
				msg += f'\n📅 {after.created_at} ➡ {after.edited_at}'
				msg += f'\n"*{before.content}*" \nto\n"*{after.content}*"'
				msg += attachmentsUrls
				await logChannelActivity.send(msg)
		except Exception as ex:
			print('----- logEditedMessage -----')
			print(ex)
