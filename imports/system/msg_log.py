from setup.properties import *
from setup.actions import *

def init_msg_log(params):
	
	bot = params['bot']
	slash = params['slash']
	purgedMsgs = []

	######################## PURGE ########################
	@slash.slash(name = "purge", description = "Clear all messages", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders', 'staff'}, {'members', 'everyone'}) })
	async def purge(ctx, limit: int=None):
		try:
			nonlocal purgedMsgs
			
			if not is_authorised(ctx, {'founders', 'staff'}):
				await ctx.send('❌ Missing Permissions')
				return
			
			purgedMsgs = []
			channelsToClear = [
				textChannels['voice-chat'],
				textChannels['help-chat']
			]
			if not limit and ctx.channel.id not in channelsToClear:
				await ctx.send('❌ Wrong Target Channel', hidden=True)
				return

			if limit:
				if limit > 500:
					await ctx.send('You cannot delete more than 500 messages', hidden=True)
					return
				else:
					await ctx.send('Clearing messages ...', hidden=True)
					deletedMsgs = await ctx.channel.purge(limit = limit, check = isNotPinned)
					await ctx.send(f'{len(deletedMsgs)} message(s) cleared', hidden=True)
					count = len(deletedMsgs)
					deletedMsgs.reverse()
					await logPurgedMessages(ctx, count, deletedMsgs)
				return

			MAX_TO_DELETE = 500
			await ctx.send('Clearing everything ...', hidden=True)
			# time.sleep(2)
			await deleteMsg(ctx, MAX_TO_DELETE)
		except Exception as ex:
			print('----- /purge() -----')
			print(ex)
			await log_exception(ex, '/purge', ctx)

	def isNotPinned(msg):
		return not msg.pinned

	async def deleteMsg(ctx, limit):
		try:
			nonlocal purgedMsgs
			deletedMsgs = await ctx.channel.purge(limit = limit, check = isNotPinned)
			purgedMsgs += deletedMsgs
			deletedMsgs = len(deletedMsgs)
			if (deletedMsgs > 0):
				return await deleteMsg(ctx, limit)
			else:
				count = len(purgedMsgs)
				purgedMsgs.reverse()
				await ctx.send(f'{len(purgedMsgs)} message(s) cleared', hidden=True)
				await logPurgedMessages(ctx, count, purgedMsgs)
				return len(purgedMsgs)
		except Exception as ex:
			print('----- deleteMsg() -----')
			print(ex)
			await log_exception(ex, 'deleteMsg()', ctx)

	async def logPurgedMessages(ctx, count, _purgedMsgs):
		log = bot.get_channel(textChannels['log-msg'])
		headerMsg = f"🗑 **purge({count}) | {ctx.channel.mention}** ──────────"
		await log.send(headerMsg)
		for m in _purgedMsgs:
			msg = '──────────────────────'
			msg += f'\n🗑 by {m.author.mention} in {m.channel.mention}'
			
			created_at = getTimeUtcPlusOne(m.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if m.edited_at:
				edited_at = getTimeUtcPlusOne(m.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n📅 {created_at} ➜ {edited_at}'
			msg_content = f'{"--Sticker | Empty--" if (m.content == "") else m.content}'
			msg += f'\n__Content__\n{msg_content}'
			msg += get_attachments(m)
			msg += get_embeds(m)
			msg += f'\n──────────────────────'
			await log.send(msg)