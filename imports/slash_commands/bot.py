
from imports.actions.common import *
from imports.actions.bot import *
from imports.data_common.slash_commands_permissions import *

def init_slash_commands_bot(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	@bot.slash_command(name="teacode")
	async def teacode(inter):
		pass

	_activity_states_data = activity_states_data(params)
	discord_states = _activity_states_data["discord_states"]
	states = _activity_states_data["states"]
	discord_activity_types = _activity_states_data["discord_activity_types"]
	activity_types = _activity_states_data["activity_types"]

	@teacode.sub_command(name = "activity")
	async def tc_bot_activity(interaction, status=commands.Param(choices=states), activity_type=commands.Param(choices=activity_types), name = None):
		"""
		Update bot activity & status
		Parameters
		----------
		status: status options list
		activity_type: activity options list
		name: value of the activity
		"""
		try:
			status = discord_states[states.index(status)]
			activity = discord_activity_types[activity_types.index(activity_type)]
			await task_update_activity(params, activity_name=name, activity_type=activity, status=status)
		except Exception as ex:
			print('----- /tc_bot_activity() -----')
			print(ex)
			await log_exception(ex, '/tc_bot_activity', interaction)

	@teacode.sub_command(name = "commands")
	async def tc_list_commands(interaction):
		"""
		List all / commands
		Parameters
		----------
		"""
		try:
			member = interaction.author
			for cmds_list in slash_commands_permissions:
				embed = discord.Embed(title=f'Bot Commands / Permission : {cmds_list}', description="", color=member.color)
				embed.set_author(name=f'{member.name}', icon_url=member.display_avatar)
				embed.set_thumbnail(url=member.display_avatar)
				for cmd_name in slash_commands_permissions[cmds_list]:
					slash_cmd = bot.get_slash_command(cmd_name)
					if slash_cmd:
						_name = slash_cmd.name
						if slash_cmd.parent:
							_name = f'{slash_cmd.parent.name} {_name}'
						embed.add_field(name=_name, value=slash_cmd.body.description, inline=True)
				embed.set_footer(text=f"🌐 Visit teacode.ma")
				await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /tc_list_commands() -----')
			print(ex)
			await log_exception(ex, '/tc_list_commands', interaction)
