from setup.data.params import * 
from setup.data.properties import *
from setup.actions.reaction import *
from setup.actions.common import *

def init_events_reaction(params):

	bot = params['bot']

	@bot.event
	async def on_raw_reaction_add(payload):
		try:
			member = payload.member
			fct_params = {
				"adding": True,
				"toggle_roles": member.add_roles,
				"action": "got",
				"member": member,
			}
			await toggleReaction(payload, fct_params)
		except Exception as ex:
			print('---------- on_raw_reaction_add(evt) --------')
			print(ex)
			await log_exception(ex, 'on_raw_reaction_add(evt)', None, bot)


	@bot.event
	async def on_raw_reaction_remove(payload):
		try:
			guild = bot.get_guild(guildId)
			member = await guild.fetch_member(payload.user_id)
			fct_params = {
				"adding": False,
				"toggle_roles": member.remove_roles,
				"action": "lost",
				"member": member,
			}
			await toggleReaction(payload, fct_params)
		except Exception as ex:
			print('---------- on_raw_reaction_remove(evt) --------')
			print(ex)
			await log_exception(ex, 'on_raw_reaction_remove(evt)', None, bot, False, payload.user_id)

	async def toggleReaction(payload, fct_params):
		excludedCategories = [
			categories['system-corner']
		]
		channel = bot.get_channel(payload.channel_id)
		if channel.category_id in excludedCategories:
			return
			
		guild = bot.get_guild(guildId)
		member = fct_params['member']

		log = bot.get_channel(textChannels['log-reaction'])
		await log_reacted_msg(params, payload, log, member, fct_params['adding'])

		if member.bot == True:
			return
		roleName = None
		if str(payload.channel_id) in reactions:
			if str(payload.message_id) in reactions[str(payload.channel_id)]:
				if str(payload.emoji) in reactions[str(payload.channel_id)][str(payload.message_id)]:
					roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
		if roleName:
			role = next(role for role in guild.roles if role.name == roleName)
			await fct_params['toggle_roles'](role)
			await log.send(f'{member.display_name}#{member.discriminator} ({member.id}) {fct_params["action"]} a role {role.mention}')