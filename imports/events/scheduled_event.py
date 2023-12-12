from imports.data_server.config import *
from imports.actions.common import *

def init_events_scheduled_event(params):
	
	bot = params['bot']
	discord = params['discord']
	
	@bot.event
	async def on_raw_guild_scheduled_event_subscribe(payload):
		try:
			guild = bot.get_guild(payload.guild_id)
			event = guild.get_scheduled_event(payload.event_id)
			msg = f'🔹 <@{payload.user_id}> subscribed to **{event.name}** / {event.id}'
			channel = bot.get_channel(textChannels['log-event'])
			await channel.send(msg)
			# if event.channel_id in voice_roles:
				# member = await guild.fetch_member(payload.user_id)
				# role = guild.get_role(voice_roles[event.channel_id])
				# await member.add_roles(role)
		except Exception as ex:
			print('----- on_raw_guild_scheduled_event_subscribe(evt) -----')
			print(ex)
			await log_exception(ex, 'on_raw_guild_scheduled_event_subscribe(evt)', None, bot)

	@bot.event
	async def on_raw_guild_scheduled_event_unsubscribe(payload):
		try:
			guild = bot.get_guild(payload.guild_id)
			event = guild.get_scheduled_event(payload.event_id)
			msg = f'🔸 <@{payload.user_id}> unsubscribed from **{event.name}** / {event.id}'
			channel = bot.get_channel(textChannels['log-event'])
			await channel.send(msg)
		except Exception as ex:
			print('----- on_raw_guild_scheduled_event_unsubscribe(evt) -----')
			print(ex)
			await log_exception(ex, 'on_raw_guild_scheduled_event_unsubscribe(evt)', None, bot)
			
	@bot.event
	async def on_guild_scheduled_event_update(before, after):
		try:
			# invite = await after.channel.create_invite(max_age=appParams['inviteForOneWeek'], max_uses=100, reason=f'Event Started Title : {after.name}')
			# event_invite_link = f'{invite}?event={after.id}'
			if before.status != after.status:
				# channel = bot.get_channel(textChannels['general'])
				# guild = bot.get_guild(guildId)
				# if after.channel_id in voice_roles:
				# 	role = guild.get_role(voice_roles[after.channel_id])
				# else:
				# 	role = guild.get_role(roles['members'])
				if after.status == discord.GuildScheduledEventStatus.active:
					await task_update_activity(params, activity_name = f'Live Now : {after.name}', activity_type = discord.ActivityType.watching)
				# 	msg = f'🟢 Live : **{after.name}** / {role.mention}\nFeel free to join\n{event_invite_link}'
				# 	await channel.send(msg.strip())
				elif after.status == discord.GuildScheduledEventStatus.completed:
					await task_update_activity(params)
				# 	msg = f'🟥 Event ended / {after.name}\nThank you for attending\nsee you soon 👋'
				# 	await channel.send(msg.strip())
		except Exception as ex:
			print('----- on_guild_scheduled_event_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_guild_scheduled_event_update(evt)', None, bot)

