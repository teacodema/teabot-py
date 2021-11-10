from database.reactions import * 
from setup.properties import *
from setup.actions import *

def init_role_reaction(params):

	bot = params['bot']
	slash = params['slash']
	get = params['get']

	@bot.event
	async def on_raw_reaction_add(payload):
		try:
			guild = bot.get_guild(guildId)
			member = payload.member

			log = bot.get_channel(textChannels['log-channel'])
			url = f'https://discord.com/channels/694956824356585654/{payload.channel_id}/{payload.message_id}'
			await log.send(f'{member.mention} Added {payload.emoji} \n{url}')

			if member.bot == True:
				return
			roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
			role = get(guild.roles, name = roleName)
			await member.add_roles(role)
		except Exception as ex:
			print('----------on_raw_reaction_add--------')
			print(ex)


	@bot.event
	async def on_raw_reaction_remove(payload):
		try:
			guild = bot.get_guild(guildId)
			member = await guild.fetch_member(payload.user_id)

			log = bot.get_channel(textChannels['log-channel'])
			url = f'https://discord.com/channels/694956824356585654/{payload.channel_id}/{payload.message_id}'
			await log.send(f'{member.mention} Removed {payload.emoji} \n{url}')

			if member.bot == True:
				return
			roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
			role = get(guild.roles, name = roleName)
			await member.remove_roles(role)
		except Exception as ex:
			print('----------on_raw_reaction_remove--------')
			print(ex)

	@slash.slash(name = "rr", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def role_react(ctx, msg_id=None):
		try:
			if msg_id:
				await ctx.send('Reactions are setting up ....', hidden=True)
				msg = await ctx.channel.fetch_message(msg_id)
				for e in reactions[str(ctx.channel.id)][msg_id]:
					await msg.add_reaction(e)
				await ctx.send('Done Reacting.', hidden=True)
				return

			await ctx.send('Updating members roles ....', hidden=True)
			guild = bot.get_guild(guildId)
			roles_assigned = 0
			for channel_id in reactions:
				channel = bot.get_channel(int(channel_id))
				for msg_id in reactions[str(channel_id)]:
					try:
						msg = await channel.fetch_message(int(msg_id))
						for r in msg.reactions:
							roleName = reactions[str(channel_id)][str(msg_id)][str(r.emoji)]
							role = get(guild.roles, name = roleName)
							async for u in r.users():
								try:
									if u.id != users['teabot']:
										member = await guild.fetch_member(u.id)
										if role not in member.roles:
											await member.add_roles(role)
											roles_assigned += 1
								except Exception as ex:
									print(ex)
									pass
					except Exception as ex:
						print(ex)
						pass
			await ctx.send(f'Done Updating members roles / {roles_assigned} updated.', hidden=True)
		except Exception as ex:
			print('----------/role_react--------')
			print(ex)