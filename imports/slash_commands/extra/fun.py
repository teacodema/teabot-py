from setup.data.properties import *
from setup.actions.common import *
import random

def init_slash_commands_extra(params):

	# client = params['client']
	bot = params['bot']
	discord = params['discord']
	inspect = params['inspect']

	######### PICK RANDOM USER #######
	@bot.slash_command(name = "pick-speaker", description = "Choose a random speaker - (events only !!)")
	async def pick_speaker(interaction):
		try:
			
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			
			await interaction.send('Choosing...')
			voice = interaction.author.voice
			if voice:
				members = voice.channel.members
				guild = bot.get_guild(guildId)
				def is_not_host_or_bot(member):
					roleIds = [role.id for role in member.roles]
					return (roles['hosts'] not in roleIds) and (not member.bot)
				members = list(filter(is_not_host_or_bot, members))
				if len(members) == 0:
					msg = 'No member chosen !! - Reasons'
					msg+= '\n- No members available in the voice channel'
					msg+= '\n- Only hosts/bot are connected for now'
					await interaction.send(msg)
					return

				member = random.choice(members)
				msg = f'Chosen member : {member.mention}'
			else:
				msg = '⚠ No busy voice channel'
			await interaction.send(msg)
		except Exception as ex:
			print('----- /random_user() -----')
			print(ex)
			await log_exception(ex, '/random_user', interaction)

	######################## JANKEN GAME ########################
	@bot.slash_command(name = "janken", description = "Rock Paper Scissors")
	async def janken(interaction, member1: discord.Member = None, member2: discord.Member = None):
		try:
			# whereToPlay = [
			# 	textChannels['general'],
			# 	textChannels['voice-chat']
			# ]

			# if (interaction.channel.id not in whereToPlay):
			# 	msg = 'You can only play in these channels:'
			# 	for c in whereToPlay:
			# 		msg += f' <#{c}>'
			# 	await interaction.send(msg)
			# 	return

			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			
			choices = [':page_facing_up:', ':scissors:', ':rock:']

			if (member1 == None and member2 == None):
				member = interaction.author
				ch = random.choice(choices)
				await interaction.send(f'__{member.display_name}__ {ch}')
				return
			else:
				if member1 == None:
					member1 = interaction.author
				elif member2 == None:
					member2 = interaction.author

			if (member1 == member2):
				await interaction.send("You can't play with yourself")
				return

			ch1 = random.choice(choices)
			ch2 = random.choice(choices)

			msg = f'__{member1.display_name}__ {ch1} **VS** {ch2} __{member2.display_name}__'
			result = ''

			index1 = choices.index(ch1)
			index2 = choices.index(ch2)

			if (index1 == 0 and index2 == 2):
				result = f'{member1.display_name} is the **WINNER** 🎉 🎊'
			elif (index2 == 0 and index1 == 2):
				result = f'{member2.display_name} is the **WINNER** 🎉 🎊'
			elif (index1 == index2):
				result = "it's a **TIE**"
			else:
				if index1 > index2:
					result = f'{member1.display_name} is the **WINNER** 🎉 🎊'
				else:
					result = f'{member2.display_name} is the **WINNER** 🎉 🎊'

			await interaction.send(f'{msg} | {result}')
		except Exception as ex:
			print('----- /janken() -----')
			print(ex)
			await log_exception(ex, '/janken', interaction)
