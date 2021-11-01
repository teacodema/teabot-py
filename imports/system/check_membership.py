from setup.properties import *
from setup.actions import *
# import schedule
# import time

def init_check_membership(params):

	bot = params['bot']
	slash = params['slash']
	get = params['get']
	
	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	# @bot.command(name="check", pass_context=True)
	@slash.slash(name="check", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def check_membership(ctx):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', hidden=True)
				return
			await ctx.send('Updating ...', hidden=True)
			updatedMembers = await checkNewMemberRole(bot, get)
			logChannel = bot.get_channel(textChannels['log-channel'])
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '

			await logChannel.send(f'{updatedMembersCount} updated members.\n{msg}')
		except Exception as ex:
			print('----- /checkMembership -----')
			print(ex)
