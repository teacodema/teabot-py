from setup.properties import *
from setup.actions import *


def init_check_membership(params):

	bot = params['bot']
	slash = params['slash']
	get = params['get']

	
	######################## CHECK UNASSIGNED MEMBERS ########################
	@slash.slash(name = "tc_cnm", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def check_new_members(ctx, nr:int=1, do:int=0):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', hidden=True)
				return
			await ctx.send('Checking ...', hidden=True)
			guild = bot.get_guild(guildId)
			def count_roles(member):
				return (len(member.roles) <= nr + 1)
			users = list(filter(count_roles, guild.members))

			_roles = [
				roles['new-members'], roles['members'],
				roles['__server_activities__'],
				roles['__techs__'], roles['__tools__'],
				roles['__jobs__'], roles['__interests__'],
			]
			roles_list = []
			for role_id in _roles:	
				role = get(guild.roles, id = role_id)
				roles_list.append(role)

			msg = ''
			for u in users:
				if do: await u.add_roles(*roles_list)
				msg += f'{u.mention} , '
			if do: await ctx.send(f'{len(users)} checked members.\n{msg}', hidden=True)
			else: await ctx.send(f'{len(users)} can be checked members.\n{msg}', hidden=True)

		except Exception as ex:
			print('----- /check_new_members() -----')
			print(ex)
			await log_exception(ex, '/check_new_members', ctx)


	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	@slash.slash(name = "tc_unm", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def update_new_members(ctx, do:int=0):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', hidden=True)
				return
			await ctx.send('Updating ...', hidden=True)
			updatedMembers = await checkNewMemberRole(bot, get, do)
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '
			if do: await ctx.send(f'{updatedMembersCount} updated members.\n{msg}', hidden=True)
			else: await ctx.send(f'{updatedMembersCount} can be updated members.\n{msg}', hidden=True)
		except Exception as ex:
			print('----- /update_new_members() -----')
			print(ex)
			await log_exception(ex, '/update_new_members', ctx)
