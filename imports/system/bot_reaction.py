from setup.reactions import * 
from setup.properties import *
from setup.actions import *

def init_bot_reaction(params):

	bot = params['bot']
	discord = params['discord']

	async def log_reacted_msg(payload, log, member, adding=True):

		url = f'https://discord.com/channels/{guildId}/{payload.channel_id}/{payload.message_id}'
		operation = f'{"Added" if adding else "Removed"}'
		await log.send(f'{url}\n{member.mention} {operation} {payload.emoji} - ({payload.emoji.id})')

		_ch = bot.get_channel(payload.channel_id)

		if _ch.category_id == categories['information']:
			return

		m = await _ch.fetch_message(payload.message_id)
		if m:
			msgs = []
			msg = f'\n✉ by {m.author.display_name} in {m.channel.mention}'
			created_at = getTimeUtcPlusOne(m.created_at, "%d %B %Y - %H:%M")
			edited_at = None
			if m.edited_at:
				edited_at = getTimeUtcPlusOne(m.edited_at, "%d %B %Y - %H:%M")
			msg += f'\n📅 {created_at} ➜ {edited_at}'
			msg += f'\n__Content__\n'
			msgs.append(msg) # await log.send(f'{msg}')
			msg_content = f'{"--Sticker | Empty--" if (m.content == "") else m.content}'
			msgs.append(msg_content) # await log.send(f'{msg_content}')
			# msg = get_attachments(m)
			# if msg: msgs.append(msg) #await log.send(msg)
			# msg = get_embeds(m)
			# if msg: msgs.append(msg) #await log.send(msg)
			# msg = f'\n──────────────────────'
			# await log.send(f'{msg}')
			for msg in msgs:
				await log.send(msg)


	@bot.event
	async def on_raw_reaction_add(payload):
		try:
			excludedCategories = [
				categories['system-corner']
			]
			channel = bot.get_channel(payload.channel_id)
			if channel.category_id in excludedCategories:
				return
				
			guild = bot.get_guild(guildId)
			member = payload.member

			log = bot.get_channel(textChannels['log-reaction'])
			await log_reacted_msg(payload, log, member)

			if member.bot == True:
				return
			roleName = None
			if str(payload.channel_id) in reactions:
				if str(payload.message_id) in reactions[str(payload.channel_id)]:
					if str(payload.emoji) in reactions[str(payload.channel_id)][str(payload.message_id)]:
						roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
			if roleName:
				role = next(role for role in guild.roles if role.name == roleName)
				await member.add_roles(role)
				await log.send(f'{member.mention} got a role {role.mention}')
		except Exception as ex:
			print('---------- on_raw_reaction_add(evt) --------')
			print(ex)
			await log_exception(ex, 'on_raw_reaction_add(evt)', None, bot)


	@bot.event
	async def on_raw_reaction_remove(payload):
		try:
			excludedCategories = [
				categories['system-corner']
			]
			channel = bot.get_channel(payload.channel_id)
			if channel.category_id in excludedCategories:
				return
				
			guild = bot.get_guild(guildId)
			member = await guild.fetch_member(payload.user_id)

			log = bot.get_channel(textChannels['log-reaction'])
			await log_reacted_msg(payload, log, member, False)

			if member.bot == True:
				return
			roleName = None
			if str(payload.channel_id) in reactions:
				if str(payload.message_id) in reactions[str(payload.channel_id)]:
					if str(payload.emoji) in reactions[str(payload.channel_id)][str(payload.message_id)]:
						roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
			if roleName:
				role = next(role for role in guild.roles if role.name == roleName)
				await member.remove_roles(role)
				await log.send(f'{member.mention} lost a role {role.mention}')
		except Exception as ex:
			print('---------- on_raw_reaction_remove(evt) --------')
			print(ex)
			await log_exception(ex, 'on_raw_reaction_remove(evt)', None, bot)


	@bot.slash_command(name = "tc_rr", description='Add/Remove reaction to/from msg - ,')
	async def bot_react(interaction, msg_id=None, emojis=None, remove:int=0, member: discord.Member = None):
		try:

			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
	
			if msg_id:
				if emojis:
					await interaction.send('Bot Reacting ....', ephemeral=True)
					msg = await interaction.channel.fetch_message(msg_id)
					emojis = emojis.split(',')
					for e in emojis:
						if remove:
							if member: await msg.remove_reaction(e, member)
							else: await msg.clear_reaction(e)
						else: await msg.add_reaction(e)
					return
				else:
					await interaction.send('Reactions are setting up ....', ephemeral=True)
					if str(interaction.channel.id) in reactions and str(msg_id) in reactions[str(interaction.channel.id)]:
						msg = await interaction.channel.fetch_message(msg_id)
						for e in reactions[str(interaction.channel.id)][msg_id]:
							await msg.add_reaction(e)
						await interaction.send('Done Reacting.', ephemeral=True)
					else: await interaction.send('Could not find channel/message.', ephemeral=True)
					return

			await interaction.send('Updating members roles ....', ephemeral=True)
			guild = bot.get_guild(guildId)
			roles_assigned = 0
			_msg = ''
			for channel_id in reactions:
				channel = bot.get_channel(int(channel_id))
				for msg_id in reactions[str(channel_id)]:
					try:
						msg = await channel.fetch_message(int(msg_id))
						for r in msg.reactions:
							roleName = reactions[str(channel_id)][str(msg_id)][str(r.emoji)]
							role = discord.utils.get(guild.roles, name = roleName)
							async for u in r.users():
								try:
									if u.id != users['teabot']:
										member = await guild.fetch_member(u.id)
										if role not in member.roles:
											await member.add_roles(role)
											_msg += f'{member.mention} got {role.mention}\n'
											roles_assigned += 1
								except Exception as ex:
									print('---------- /bot_react()/add role user --------')
									print(ex)
									print(role.name)
									print(u.name)
									await msg.remove_reaction(r.emoji, u)
									pass
					except Exception as ex:
						print('---------- /bot_react()/msg reactions --------')
						print(ex)
						print(channel.name)
						print(role.name)
						pass
			await interaction.send(f'Done Updating members roles / {roles_assigned} updated.\n{_msg}', ephemeral=True)
		except Exception as ex:
			print('---------- /bot_react() --------')
			print(ex)
			await log_exception(ex, '/bot_react', interaction)