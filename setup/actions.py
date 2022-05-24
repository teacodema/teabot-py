from datetime import datetime
import pytz
from setup.properties import *

async def log_exception(ex, action, interaction=None, bot=None, hidden=True, msg=None):
	try:
		if msg: msg += f'\n----\n{action}\n{str(ex)}'
		else: msg = f'{action}\n{str(ex)}'
		if interaction:
			await interaction.send(msg, ephemeral = hidden)
		elif bot:
			logBot = bot.get_channel(textChannels['log-exception'])
			await logBot.send(msg)
	except Exception as ex:
		print('----- log_exception -----')
		print(ex)


def is_authorised(interaction, authorizedRolesIds):
	roleIds = [role.id for role in interaction.author.roles]
	authorizedRoles = list({key: roles[key] for key in authorizedRolesIds}.values())
	roleExists = [value for value in authorizedRoles if value in roleIds]
	return len(roleExists) > 0

def is_founders(interaction):
	return is_authorised(interaction, {'founders'})

# def slash_permissions(authorizedRolesIds, unAuthorizedRolesIds):
# 	permissions = []
# 	if authorizedRolesIds:
# 		authorizedRoles = list({key: roles[key] for key in authorizedRolesIds}.values())
# 		for r in authorizedRoles:
# 			permissions.append(create_permission(r, SlashCommandPermissionType.ROLE, True))
# 	if unAuthorizedRolesIds:
# 		unAuthorizedRoles = list({key: roles[key] for key in unAuthorizedRolesIds}.values())
# 		for r in unAuthorizedRoles:
# 			permissions.append(create_permission(r, SlashCommandPermissionType.ROLE, False))
# 	return permissions

def get_attachments(message):
	if len(message.attachments):
		attachmentsUrls = '\n__Attachments__\n'
		for attch in message.attachments:
			attachmentsUrls += f'{attch.url}\n'
		return attachmentsUrls
	return ''

def get_embeds(message):
	if len(message.embeds):
		embedsUrls = '\n__Embeds__\n'
		for attch in message.embeds:
			embedsUrls += f'{attch.url} - {attch.image} - {attch.author.mention} - {attch.description}\n'
		return embedsUrls
	return ''

async def checkNewMemberRole(guild, do:int=0):
	try:
		role = guild.get_role(roles['new-members'])
		updated = []
		for member in role.members:
			diff = datetime.now() - member.joined_at.replace(tzinfo=None)
			if diff.days >= appParams['newMembershipPeriode']:
				updated.append(member.mention)
				if do: await member.remove_roles(role)
		return updated
	except Exception as ex:
		print('----- checkNewMemberRole -----')
		print(ex)
		return -1

def getTimeUtcPlusOne(dt, format = "%d %B %Y - %H:%M"):
	timeZ_Ma = pytz.timezone('Africa/Casablanca')
	dt_Ma = dt.astimezone(timeZ_Ma).strftime(format)
	return dt_Ma


def replace_str(str, dict_chars):
	try:
		for key in dict_chars:
			str = str.replace(key, dict_chars[key])
		return str
	except Exception as ex:
		print('----- replace_str() -----')
		print(ex)
