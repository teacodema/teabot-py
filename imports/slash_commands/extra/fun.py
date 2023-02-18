import random
from imports.data_server.config import *
from imports.actions.common import *

def init_slash_commands_fun(params):

	# client = params['client']
	bot = params['bot']
	discord = params['discord']
	
	@bot.slash_command(name="fun")
	async def fun(inter):
		pass

	######################## JANKEN GAME ########################
	@fun.sub_command(name = "janken", description = "Rock Paper Scissors")
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
				await interaction.send("You can't play with yourself", ephemeral=True)
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


	####################### MAKE A WEBHOOK #######################
	@fun.sub_command(name = "make-webhook")
	async def tc_make_webhook(interaction, member: discord.Member, channel: discord.abc.GuildChannel, msg, name=None):
		"""
		Make a webhook - \\n \\t /$
		Parameters
		----------
		member: Server existing member
		msg: Message to send by the webhook - \\n \\t /$
		channel: Channel where to send the msg
		name: Webhook name
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			if name == None:
				name = member.display_name
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})
			webhook = await channel.create_webhook(name=name)
			await webhook.send(f'{msg}', username=name, avatar_url=member.display_avatar.url)
			await webhook.delete()
			await interaction.send('✅ Webhook made', ephemeral=True)
		except Exception as ex:
			await interaction.send('❌ Webhook not made', ephemeral=True)
			print('----- /tc_make_webhook() -----')
			print(ex)
			await log_exception(ex, '/tc_make_webhook', interaction)
	