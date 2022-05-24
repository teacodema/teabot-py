from setup.properties import *
from setup.actions import *

def init_msg_log(params):
	
	bot = params['bot']
	purgedMsgs = []

	######################## PURGE ########################
	@bot.slash_command(name = "purge", description = "Clear all messages")
	async def purge(interaction, limit: int=None):
		try:
			nonlocal purgedMsgs
			
			if not is_authorised(interaction, {'founders', 'staff'}):
				await interaction.send('❌ Missing Permissions')
				return
			
			purgedMsgs = []
			channelsToClear = [
				textChannels['voice-chat']
			]
			if not limit and interaction.channel.id not in channelsToClear:
				await interaction.send('❌ Wrong Target Channel', ephemeral=True)
				return

			if limit:
				if limit > 500:
					await interaction.send('You cannot delete more than 500 messages', ephemeral=True)
					return
				else:
					await interaction.send('Clearing messages ...', ephemeral=True)
					deletedMsgs = await interaction.channel.purge(limit = limit, check = isNotPinned)
					await interaction.send(f'{len(deletedMsgs)} message(s) cleared', ephemeral=True)
					count = len(deletedMsgs)
					deletedMsgs.reverse()
					await logPurgedMessages(interaction, count, deletedMsgs)
				return

			MAX_TO_DELETE = 500
			await interaction.send('Clearing everything ...', ephemeral=True)
			# time.sleep(2)
			await deleteMsg(interaction, MAX_TO_DELETE)
		except Exception as ex:
			print('----- /purge() -----')
			print(ex)
			await log_exception(ex, '/purge', interaction)

	def isNotPinned(msg):
		return not msg.pinned

	async def deleteMsg(interaction, limit):
		try:
			nonlocal purgedMsgs
			deletedMsgs = await interaction.channel.purge(limit = limit, check = isNotPinned)
			purgedMsgs += deletedMsgs
			deletedMsgs = len(deletedMsgs)
			if (deletedMsgs > 0):
				return await deleteMsg(interaction, limit)
			else:
				count = len(purgedMsgs)
				purgedMsgs.reverse()
				await interaction.send(f'{len(purgedMsgs)} message(s) cleared', ephemeral=True)
				await logPurgedMessages(interaction, count, purgedMsgs)
				return len(purgedMsgs)
		except Exception as ex:
			print('----- deleteMsg() -----')
			print(ex)
			await log_exception(ex, 'deleteMsg()', interaction)

	async def logPurgedMessages(interaction, count, _purgedMsgs):
		log = bot.get_channel(textChannels['log-msg'])
		headerMsg = f"🗑 **purge({count}) | {interaction.channel.mention}** ──────────"
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