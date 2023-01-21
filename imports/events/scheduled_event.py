from imports.data_server.config import *
from imports.actions.common import *

def init_events_scheduled_event(params):
	
	bot = params['bot']
	
	@bot.event
	async def on_raw_guild_scheduled_event_subscribe(payload):
		try:
			guild = bot.get_guild(guildId)
			event = guild.get_scheduled_event(payload.event_id)
			if event.channel_id in voice_roles:
				member = await guild.fetch_member(payload.user_id)
				role = guild.get_role(voice_roles[event.channel_id])
				await member.add_roles(role)
		except Exception as ex:
			print('----- on_raw_guild_scheduled_event_subscribe(evt) -----')
			print(ex)
			await log_exception(ex, 'on_raw_guild_scheduled_event_subscribe(evt)', None, bot)