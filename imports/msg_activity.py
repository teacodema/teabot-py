from setup.properties import *
from setup.actions import *


def init_msg_activity(params):
	
	client = params['client']
	slash = params['slash']
	purgedMsgs = []

	######################## BULK MSG DELETION ########################
	@slash.slash(name="clear", description="Clear messages (0 .. 500)", guild_ids=[guildId])
	async def clear(ctx, number: int):
		try:
			await clearMsg(ctx, number)
		except Exception as ex:
			print('----- /clear -----')
			print(ex)


	######################## BULK MSG DELETION ########################
	@slash.slash(name="clearall", description="Clear all messages", guild_ids=[guildId])
	async def clearall(ctx):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			channelId = ctx.channel.id
			channelsToClear = [
				textChannels['voice-chat'],
				textChannels['help-chat']
			]
			if (channelId not in channelsToClear):
				await ctx.send('❌ Wrong Target Channel', delete_after = 2)
				return

			MAX_TO_DELETE = 500
			await ctx.send('Clearing everything ...', delete_after = 2)
			# time.sleep(2)
			await deleteMsg(ctx, MAX_TO_DELETE)
		except Exception as ex:
			print('----- /clearall -----')
			print(ex)

	async def deleteMsg(ctx, limit):
		try:
			deletedMsgs = await ctx.channel.purge(limit = limit)
			nonlocal purgedMsgs
			purgedMsgs += deletedMsgs
			deletedMsgs = len(deletedMsgs)
			if (deletedMsgs > 0):
				return await deleteMsg(ctx, limit)
			else:
				logMsgsChannel = client.get_channel(textChannels['log-msg'])
				headerMsg = f"----------❌ **ClearAll() | {ctx.channel.mention}** ❌----------------------------------------"
				await logMsgsChannel.send(headerMsg)
				for m in purgedMsgs:
					msg = f'💢 by {m.author.mention} in {m.channel.mention}'
					msg += f'\n📅 {m.created_at} ➡ {m.edited_at}'
					msg += f'\n"*{m.content}*"'
					msg += f'\n----------------------------------------------'
					await logMsgsChannel.send(msg)
				purgedMsgs = []
				return
		except Exception as ex:
			print('----- deleteMsg -----')
			print(ex)

	######################## BULK MSG DELETION ########################
	async def clearMsg(ctx, number):
		try:

			roleIds = [role.id for role in ctx.author.roles]
			authorizedRoles = [roles['founders'], roles['moderators']]
			if not is_authorised(roleIds, authorizedRoles):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			if (number > 500):
				await ctx.send('You cannot delete more than 500 messages', delete_after = 2)
				return
			else:
				await ctx.send('Clearing messages ...', delete_after = 2)
				deletedMsgs = await ctx.channel.purge(limit = number + 1)
				await ctx.send(f'{len(deletedMsgs) - 1} message(s) cleared', delete_after = 2)

				count = len(deletedMsgs)
				logMsgsChannel = client.get_channel(textChannels['log-msg'])
				headerMsg = f"----------❌ **Clear({count}) | {ctx.channel.mention}** ❌----------------------------------------"
				await logMsgsChannel.send(headerMsg)
				for m in deletedMsgs:
					msg = f'💢 by {m.author.mention} in {m.channel.mention}'
					msg += f'\n📅 {m.created_at} ➡ {m.edited_at}'
					msg += f'\n"*{m.content}*"'
					msg += f'\n----------------------------------------------'
					await logMsgsChannel.send(msg)
				
		except Exception as ex:
			print('----- clearMsg -----')
			print(ex)

