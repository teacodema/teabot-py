from setup.properties import *
from setup.actions import *
# import schedule
# import time

def init_check_membership(params):

	client = params['client']
	slash = params['slash']
	get = params['get']

	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	@slash.slash(name="check-membership", guild_ids=[guildId])
	async def check_membership(ctx):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			await ctx.send('Updating ...', delete_after = 2)
			updatedMembers = await checkNewMemberRole(client, get)
			logChannel = client.get_channel(textChannels['log-channel'])
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '

			await logChannel.send(f'{updatedMembersCount} updated members.\n{msg}')
		except Exception as ex:
			print('----- /checkMembership -----')
			print(ex)
