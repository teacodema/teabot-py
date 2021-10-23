from datetime import datetime
from setup.properties import *


def is_authorised(roleIds, authorizedRoles):
	roleExists = [value for value in authorizedRoles if value in roleIds]
	return len(roleExists) > 0

def is_founders(ctx):
	roleIds = [role.id for role in ctx.author.roles]
	authorizedRoles = [roles['founders']]

	return is_authorised(roleIds, authorizedRoles)


async def checkNewMemberRole(bot, get):
	try:
		guild = bot.get_guild(guildId)
		role = get(guild.roles, id = roles['new-members'])
		updated = []
		for member in role.members:
			diff = datetime.now() - member.joined_at
			if diff.days >= newMembershipPeriode:
				updated.append(member.mention)
				await member.remove_roles(role)
		return updated
	except Exception as ex:
		print('----- checkNewMemberRole -----')
		print(ex)
		return -1