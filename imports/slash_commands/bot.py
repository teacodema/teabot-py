
from imports.actions.common import *
from imports.data_common.slash_commands_permissions import *

def init_slash_commands_bot(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	states = ["online", "dnd", "idle", "offline", "streaming"]
	discord_states = [ discord.Status.online, discord.Status.dnd, discord.Status.idle, discord.Status.offline, discord.Status.streaming]
	activity_types = ["watching", "listening", "playing", "streaming", "competing"]
	discord_activity_types = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing, discord.ActivityType.streaming, discord.ActivityType.competing]

	@bot.slash_command(name = "activity", description = "Edit bot activity & status")
	async def tc_bot_activity(interaction, status=commands.Param(choices=states), activity_type=commands.Param(choices=activity_types), name = None):
		try:
			status = discord_states[states.index(status)]
			if name == None:
				name = "🌐 teacode.ma ☕"
			activity = discord.Activity(type = discord_activity_types[activity_types.index(activity_type)], name=name)
			await bot.change_presence(status=status, activity=activity)
		except Exception as ex:
			print('----- /tc_bot_activity() -----')
			print(ex)
			await log_exception(ex, '/tc_bot_activity', interaction)

	@bot.slash_command(name = "list-commands", description = "List all / commands")
	async def tc_list_commands(interaction):
		member = interaction.author
		for cmds_list in slash_commands_permissions:
			embed = discord.Embed(title=f'Bot Commands / Permission : {cmds_list}', description="", color=member.color)
			embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.display_avatar)
			embed.set_thumbnail(url=member.display_avatar)
			for cmd_name in slash_commands_permissions[cmds_list]:
				slash_cmd = bot.get_slash_command(cmd_name)
				if slash_cmd:
					embed.add_field(name=slash_cmd.name, value=slash_cmd.body.description, inline=True)
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await interaction.send(embed=embed, ephemeral=True)
