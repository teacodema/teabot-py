from datetime import datetime
from setup.properties import *
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

async def log_exception(ex, action, ctx=None, bot=None, hidden = True):
	msg = f'{action}\n{str(ex)}'
	if ctx:
		await ctx.send(msg, hidden = hidden)
	elif bot:
		logBot = bot.get_channel(textChannels['log-bot'])
		await logBot.send(msg)

def is_authorised(ctx, authorizedRolesIds):
	roleIds = [role.id for role in ctx.author.roles]
	authorizedRoles = list({key: roles[key] for key in authorizedRolesIds}.values())
	roleExists = [value for value in authorizedRoles if value in roleIds]
	return len(roleExists) > 0

def is_founders(ctx):
	return is_authorised(ctx, {'founders'})

def slash_permissions(authorizedRolesIds, unAuthorizedRolesIds):
	permissions = []

	authorizedRoles = list({key: roles[key] for key in authorizedRolesIds}.values())
	for r in authorizedRoles:
		permissions.append(create_permission(r, SlashCommandPermissionType.ROLE, True))

	unAuthorizedRoles = list({key: roles[key] for key in unAuthorizedRolesIds}.values())
	for r in unAuthorizedRoles:
		permissions.append(create_permission(r, SlashCommandPermissionType.ROLE, False))

	return permissions

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