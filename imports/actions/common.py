# from database.player import *
from imports.data.server.channels_categories import *
from imports.data.server.members_roles import *
from imports.data.common.slash_commands_permissions import *
import pytz, re


def is_not_host_or_bot(member):
	roleIds = [role.id for role in member.roles]
	return (roles['hosts'] not in roleIds) and (not member.bot)

def start_task(task):
	try:
		task.start()
	except:
		pass

def end_task(task):
	try:
		task.cancel()
	except:
		pass
		
async def log_exception(ex, action, interaction=None, bot=None, hidden=True, msg=None):
	try:
		if msg: msg += f'\n----\n{action}\n{str(ex)}'
		else: msg = f'{action}\n{str(ex)}'
		msg += '\n──────────────────────'
		if interaction:
			await interaction.send(msg.strip(), ephemeral = hidden)
		elif bot:
			logBot = bot.get_channel(textChannels['log-exception'])
			await logBot.send(msg.strip())
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

def is_allowed(interaction, action_name):
	# for role_id in slash_commands_permissions[action_name]:
	# 	role = interaction.guild.get_role(roles[role_id])
	# 	if role in interaction.author.roles:
	# 		return True
	if action_name in slash_commands_permissions['members']:
		return True
	rootRole = interaction.guild.get_role(roles['root'])
	if rootRole in interaction.author.roles:
		return True
	roles_keys = [ role for role in slash_commands_permissions ]
	for role_key in roles_keys:
		if role_key in roles:
			role = interaction.guild.get_role(roles[role_key])
			if role in interaction.author.roles and action_name in slash_commands_permissions[role_key]:
				return True
	return False

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

def split_str(str, spliters=None):
	try:
		if spliters:
			return re.split(spliters, str)
		return re.split(',| |;|-|_', str)
	except Exception as ex:
		print('----- split_str() -----')
		print(ex)


def task_update_activity(params, activity_name = None):
	bot = params['bot']
	discord = params['discord']
	tasks = params['tasks']
	@tasks.loop(count=1, reconnect=False)
	async def update_activity():
		if activity_name:
			activity = discord.Activity(type = discord.ActivityType.playing, name = activity_name)
		else:
			activity = discord.Activity(type=discord.ActivityType.watching, name="🌐 teacode.ma ☕")
		await bot.change_presence(activity = activity)
	update_activity.start()
