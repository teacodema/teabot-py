from setup.properties import *
from setup.actions import *
import pytz

def init_msg_log(params):
	
	bot = params['bot']
	slash = params['slash']
	purgedMsgs = []

	######################## CLEAR ########################
	@slash.slash(name="clear", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders', 'moderators'}, {'members', 'everyone'}) })
	async def clear(ctx, number: int):
		try:
			if not is_authorised(ctx, {'founders', 'moderators'}):
				await ctx.send('❌ Missing Permissions')
				return
			if (number > 500):
				await ctx.send('You cannot delete more than 500 messages', hidden=True)
				return
			else:
				await ctx.send('Clearing messages ...', hidden=True)
				deletedMsgs = await ctx.channel.purge(limit = number + 1, check = isNotPinned, oldest_first=True)
				await ctx.send(f'{len(deletedMsgs)} message(s) cleared', hidden=True)

				count = len(deletedMsgs)
				# deletedMsgs.reverse()
				logMsgsChannel = bot.get_channel(textChannels['log-msg'])
				headerMsg = f"🗑 **clear({count}) | {ctx.channel.mention}** ──────────"
				await logMsgsChannel.send(headerMsg)
				for m in deletedMsgs:
					msg = '──────────────────────'
					msg += f'\n🗑 by {m.author.mention} in {m.channel.mention}'
					
					timeZ_Ma = pytz.timezone('Africa/Casablanca')
					created_at = m.created_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
					edited_at = None
					if m.edited_at:
						edited_at =  m.edited_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
					msg += f'\n📅 {created_at} ➜ {edited_at}'
					msg += f'\n__Content__\n{m.content}'
					msg += get_attachments(m)
					msg += get_embeds(m)
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
			nonlocal purgedMsgs
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			
			purgedMsgs = []
			channelId = ctx.channel.id
			channelsToClear = [
				textChannels['voice-chat'],
				textChannels['help-chat'],
				textChannels['activities-notes']
			]
			if (channelId not in channelsToClear):
				await ctx.send('❌ Wrong Target Channel', hidden=True)
				return

			MAX_TO_DELETE = 500
			await ctx.send('Clearing everything ...', hidden=True)
			# time.sleep(2)
			await deleteMsg(ctx, MAX_TO_DELETE)
			await ctx.send(f'{len(purgedMsgs)} message(s) cleared', hidden=True)
		except Exception as ex:
			print('----- /purge -----')
			print(ex)

	def isNotPinned(msg):
		return not msg.pinned

	async def deleteMsg(ctx, limit):
		try:
			nonlocal purgedMsgs
			deletedMsgs = await ctx.channel.purge(limit = limit, check = isNotPinned, oldest_first=True)
			purgedMsgs += deletedMsgs
			deletedMsgs = len(deletedMsgs)
			if (deletedMsgs > 0):
				return await deleteMsg(ctx, limit)
			else:
				count = len(purgedMsgs)
				# purgedMsgs.reverse()
				logMsgsChannel = bot.get_channel(textChannels['log-msg'])
				headerMsg = f"🗑 **purge({count}) | {ctx.channel.mention}** ──────────"
				await logMsgsChannel.send(headerMsg)
				for m in purgedMsgs:
					msg = '──────────────────────'
					msg += f'\n🗑 by {m.author.mention} in {m.channel.mention}'
					
					timeZ_Ma = pytz.timezone('Africa/Casablanca')
					created_at = m.created_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")
					edited_at = None
					if m.edited_at:
						edited_at =  m.edited_at.astimezone(timeZ_Ma).strftime("%d %B %Y - %H:%M")	
					msg += f'\n📅 {created_at} ➜ {edited_at}'
					msg += f'\n__Content__\n{m.content}'
					msg += get_attachments(m)
					msg += get_embeds(m)
					msg += f'\n──────────────────────'
					await logMsgsChannel.send(msg)
				return len(purgedMsgs)
		except Exception as ex:
			print('----- deleteMsg -----')
			print(ex)
