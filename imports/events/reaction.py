from setup.data.params import * 
from setup.data.properties import *
from setup.actions.reaction import *
from setup.actions.common import *
from setup.actions.message import *

def init_events_reaction(params):

	bot = params['bot']

	@bot.event
	async def on_raw_reaction_add(payload):
		try:
			member = payload.member
			if not member: 
				guild = bot.get_guild(guildId)
				member = await guild.fetch_member(payload.user_id)
			fct_params = {
				"adding": True,
				"toggle_roles": (member.add_roles if hasattr(member, 'add_roles') else None),
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
				"toggle_roles": (member.remove_roles if hasattr(member, 'remove_roles') else None),
				"action": "lost",
				"member": member,
			}
			await toggleReaction(payload, fct_params)
		except Exception as ex:
			print('---------- on_raw_reaction_remove(evt) --------')
			print(ex)
			await log_exception(ex, 'on_raw_reaction_remove(evt)', None, bot, False, str(payload.user_id))

	async def toggleReaction(payload, fct_params):
		try:
			log = bot.get_channel(textChannels['log-reaction'])
			
				
			guild = bot.get_guild(guildId)
			member = fct_params['member']

			log_thread = await log_reacted_msg(params, payload, log, member, fct_params['adding'])

			if member.bot != True:
				roleName = None
				if str(payload.channel_id) in reactions:
					if str(payload.message_id) in reactions[str(payload.channel_id)]:
						if str(payload.emoji) in reactions[str(payload.channel_id)][str(payload.message_id)]:
							roleName = reactions[str(payload.channel_id)][str(payload.message_id)][str(payload.emoji)]
				if roleName and "toggle_roles" in fct_params:
					role = next(role for role in guild.roles if role.name == roleName)
					await fct_params['toggle_roles'](role)
					user_mention = toggle_user_mention(member, roles['mods'], True)
					await log_thread.send(f'{user_mention} {fct_params["action"]} a role {role.mention}')
			await log_thread.edit(archived=True)
		except Exception as ex:
			raise ex