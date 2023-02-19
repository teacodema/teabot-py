from imports.actions.common import *
from imports.data_common.rules import *

def init_slash_commands_guide(params):

	bot = params['bot']
	commands = params['commands']

	@bot.slash_command(name="guide")
	async def guide(inter):
		pass

	keys = [ rule['key'] for rule in rules ]
	######### RULES ########
	@guide.sub_command(name = "tag-rule")
	async def tag_rules(interaction, query=commands.Param(choices=keys)):
		"""
		Reminde with a rule
		Parameters
		----------
		query: Choose a predefined rule by key
		"""
		try:
			if query not in keys:
				await interaction.send('⚠ Issue with the input (choose one of the provided options)', ephemeral=True)
				return
			rule = next(item for item in rules if item["key"] == query)
			# rule_index = rules.index(rule) + 1
			msg = f'**{query} :**\n{rule["value"]}'
			await interaction.send(msg.strip())
		except Exception as ex:
			print('----- /tag_rules() -----')
			print(ex)
			await log_exception(ex, '/tag_rules', interaction)
