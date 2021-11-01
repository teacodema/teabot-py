import emoji
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
			if member.bot == True:
				return
			roleName = reactions[str(payload.message_id)][str(payload.emoji)]
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
			if member.bot == True:
				return
			roleName = reactions[str(payload.message_id)][str(payload.emoji)]
			role = get(guild.roles, name = roleName)
			await member.remove_roles(role)
		except Exception as ex:
			print('----------on_raw_reaction_remove--------')
			print(ex)

	@slash.slash(name = "rr", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def role_react(ctx, msg_id):
		try:
			await ctx.send('Reactions are setting up ....', hidden=True)
			msg = await ctx.channel.fetch_message(msg_id)
			for e in reactions[msg_id]:
				# print(e, reactions[msg_id][e])
				# print('----------')
				await msg.add_reaction(e)
		except Exception as ex:
			print('----------/role_react--------')
			print(ex)