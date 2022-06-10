from setup.properties import *
from setup.actions import *
from setup.rules import *

def init_rules_tag(params):
	bot = params['bot']
	commands = params['commands']

	keys = [ rule['key'] for rule in rules ]
	######### RULES ########
	@bot.slash_command(name = "tag", description = "Reminde with a rule")
	async def tag_rules(interaction, query=commands.Param(autocomplete=keys)):
		try:
			rule = next(item for item in rules if item["key"] == query)
			rule_index = rules.index(rule) + 1
			msg = f'📕・{rule_index} - {rule["value"]}\n\n➜ Check <#{textChannels["rules"]}> for more rules'
			await interaction.send(msg)
		except Exception as ex:
			print('----- /tag_rules() -----')
			print(ex)
			await log_exception(ex, '/tag_rules', interaction)
