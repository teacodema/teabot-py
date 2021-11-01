
import random
from setup.properties import *

def init_fun_activity(params):
	
	# client = params['client']
	discord = params['discord']
	slash = params['slash']

	######################## JANKEN GAME ########################
	@slash.slash(name = "janken", description = "Rock Paper Scissors", guild_ids=[guildId])
	async def janken(ctx, member1: discord.Member = None, member2: discord.Member = None):
		try:
			# whereToPlay = [
			# 	textChannels['general'],
			# 	textChannels['voice-chat']
			# ]

			# if (ctx.channel.id not in whereToPlay):
			# 	msg = 'You can only play in these channels:'
			# 	for c in whereToPlay:
			# 		msg += f' <#{c}>'
			# 	await ctx.send(msg)
			# 	return

			choices = [':page_facing_up:', ':scissors:', ':rock:']

			if (member1 == None and member2 == None):
				member = ctx.author
				ch = random.choice(choices)
				await ctx.send(f'{member.mention} {ch}')
				return
			else:
				if (member1 == None):
					member1 = ctx.author
				elif (member2 == None):
					member2 = ctx.author

			if (member1 == member2):
				await ctx.send("You can't play with yourself")
				return

			ch1 = random.choice(choices)
			ch2 = random.choice(choices)

			msg = f'{member1.mention} {ch1} vs {ch2} {member2.mention}'
			result = ''

			index1 = choices.index(ch1)
			index2 = choices.index(ch2)

			if (index1 == 0 and index2 == 2):
				result = f'**{member1.mention}** is the **WINNER**'
			elif (index2 == 0 and index1 == 2):
				result = f'**{member2.mention}** is the **WINNER**'
			elif (index1 == index2):
				result = "it's a **TIE**"
			else:
				if (index1 > index2):
					result = f'**{member1.mention}** is the **WINNER**'
				else:
					result = f'**{member2.mention}** is the **WINNER**'

			await ctx.send(f'{msg} | {result}')
		except Exception as ex:
			print('----- /janken -----')
			print(ex)
