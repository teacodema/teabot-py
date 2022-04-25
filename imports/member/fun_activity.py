from setup.properties import *
from setup.actions import *
import random

def init_fun_activity(params):
	
	# client = params['client']
	bot = params['bot']
	discord = params['discord']
	slash = params['slash']
	get = params['get']

	######### PICK RANDOM USER #######
	@slash.slash(name = "pick-speaker", description = "Choose a random speaker - (events only !!)", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders', 'staff', 'hosts'}, {'members', 'everyone'}) })
	async def pick_speaker(ctx):
		try:
			await ctx.send('Choosing...')
			voice = ctx.author.voice
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
					await ctx.send(msg)
					return

				member = random.choice(members)
				msg = f'Chosen member : {member.mention}'
			else:
				msg = '⚠ No busy voice channel'
			await ctx.send(msg)
		except Exception as ex:
			print('----- /random_user() -----')
			print(ex)
			await log_exception(ex, '/random_user', ctx)

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
				await ctx.send(f'__{member.display_name}__ {ch}')
				return
			else:
				if member1 == None:
					member1 = ctx.author
				elif member2 == None:
					member2 = ctx.author

			if (member1 == member2):
				await ctx.send("You can't play with yourself")
				return

			ch1 = random.choice(choices)
			ch2 = random.choice(choices)

			msg = f'__{member1.display_name}__ {ch1} **VS** {ch2} __{member2.display_name}__'
			result = ''

			index1 = choices.index(ch1)
			index2 = choices.index(ch2)

			if (index1 == 0 and index2 == 2):
				result = f'{member1.mention} is the **WINNER** 🎉 🎊'
			elif (index2 == 0 and index1 == 2):
				result = f'{member2.mention} is the **WINNER** 🎉 🎊'
			elif (index1 == index2):
				result = "it's a **TIE**"
			else:
				if index1 > index2:
					result = f'{member1.mention} is the **WINNER** 🎉 🎊'
				else:
					result = f'{member2.mention} is the **WINNER** 🎉 🎊'

			await ctx.send(f'{msg} | {result}')
		except Exception as ex:
			print('----- /janken() -----')
			print(ex)
			await log_exception(ex, '/janken', ctx)
