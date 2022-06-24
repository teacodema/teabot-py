from setup.actions.common import *

######################## TOGGLE ROLE ########################
async def toggleRole(member, roles, assign = True, interaction = None):
	try:
		if assign:
			await member.add_roles(*roles)
		else:
			await member.remove_roles(*roles)
	except Exception as ex:
		print('----- toggleRole() -----')
		print(ex)
		await log_exception(ex, 'toggleRole()', interaction)
		