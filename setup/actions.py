from setup.properties import *

def is_authorised(roleIds, authorizedRoles):
	roleExists = [value for value in authorizedRoles if value in roleIds]
	return len(roleExists) > 0

def is_founders(ctx):
	roleIds = [role.id for role in ctx.author.roles]
	authorizedRoles = [roles['founders']]

	return is_authorised(roleIds, authorizedRoles)