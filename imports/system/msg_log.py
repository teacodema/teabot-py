from setup.properties import *
from setup.actions import *


def init_msg_log(params):
	
	bot = params['bot']
	slash = params['slash']
	purgedMsgs = []

	######################## CLEAR ########################
	@slash.slash(name="clear", description="Clear messages (0 .. 500)", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders', 'moderators'}, {'members', 'everyone'}) })
	async def clear(ctx, number: int):
		try:
			if not is_authorised(ctx, {'founders', 'moderators'}):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			if (number > 500):
				await ctx.send('You cannot delete more than 500 messages', delete_after = 2)
				return
			else:
				await ctx.send('Clearing messages ...', delete_after = 2)
				deletedMsgs = await ctx.channel.purge(limit = number + 1, check = isNotPinned)
				await ctx.send(f'{len(deletedMsgs) - 1} message(s) cleared', delete_after = 2)

				count = len(deletedMsgs)
				deletedMsgs.reverse()
				logMsgsChannel = bot.get_channel(textChannels['log-msg'])
				headerMsg = f"❌ **clear({count}) | {ctx.channel.mention}** ──────────"
				await logMsgsChannel.send(headerMsg)
				for m in deletedMsgs:
					msg = '──────────────────────'
					msg += f'\n💢 by {m.author.mention} in {m.channel.mention}'
					msg += f'\n📅 {m.created_at} ➡ {m.edited_at}'
					msg += f'\n__Content__\n{m.content}'
					if len(m.attachments):
						attachmentsUrls = '\n__Attachments__\n'
						for attch in m.attachments:
							attachmentsUrls += f'{attch.url}\n'
						msg += attachmentsUrls
					if len(m.embeds):
						embedsUrls = '\n__Embeds__\n'
						for attch in m.embeds:
							embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
						msg += embedsUrls
					msg += f'\n──────────────────────'
					await logMsgsChannel.send(msg)
		except Exception as ex:
			print('----- /clear -----')
			print(ex)


	######################## PURGE ########################
	@slash.slash(name="purge", description="Clear all messages", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def purge(ctx):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			channelId = ctx.channel.id
			channelsToClear = [
				textChannels['voice-chat'],
				textChannels['help-chat'],
				textChannels['activities-notes']
			]
			if (channelId not in channelsToClear):
				await ctx.send('❌ Wrong Target Channel', delete_after = 2)
				return

			MAX_TO_DELETE = 500
			await ctx.send('Clearing everything ...', delete_after = 2)
			# time.sleep(2)
			await deleteMsg(ctx, MAX_TO_DELETE)
		except Exception as ex:
			print('----- /purge -----')
			print(ex)

	def isNotPinned(msg):
		return not msg.pinned

	async def deleteMsg(ctx, limit):
		try:
			deletedMsgs = await ctx.channel.purge(limit = limit, check = isNotPinned)
			nonlocal purgedMsgs
			purgedMsgs += deletedMsgs
			deletedMsgs = len(deletedMsgs)
			if (deletedMsgs > 0):
				return await deleteMsg(ctx, limit)
			else:
				count = len(purgedMsgs)
				purgedMsgs.reverse()
				logMsgsChannel = bot.get_channel(textChannels['log-msg'])
				headerMsg = f"❌ **purge({count}) | {ctx.channel.mention}** ──────────"
				await logMsgsChannel.send(headerMsg)
				for m in purgedMsgs:
					msg = '──────────────────────'
					msg += f'\n💢 by {m.author.mention} in {m.channel.mention}'
					msg += f'\n📅 {m.created_at} ➡ {m.edited_at}'
					msg += f'\n__Content__\n{m.content}'
					if len(m.attachments):
						attachmentsUrls = '\n__Attachments__\n'
						for attch in m.attachments:
							attachmentsUrls += f'{attch.url}\n'
						msg += attachmentsUrls
					if len(m.embeds):
						embedsUrls = '\n__Embeds__\n'
						for attch in m.embeds:
							embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
						msg += embedsUrls
					msg += f'\n──────────────────────'
					await logMsgsChannel.send(msg)
				purgedMsgs = []
				return
		except Exception as ex:
			print('----- deleteMsg -----')
			print(ex)
