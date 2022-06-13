from setup.data.params import * 
from setup.data.properties import *
from setup.actions.reaction import *
from setup.actions.common import *

def init_events_reaction(params):

	bot = params['bot']

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
			await log_reacted_msg(params, payload, log, member)

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
			await log_reacted_msg(params, payload, log, member, False)

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

