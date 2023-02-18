import requests, os
import dateutil.parser as dp
import dateutil.relativedelta as drel
from datetime import timedelta, timezone
from imports.data_common.config import *
from imports.actions.common import *
from imports.actions.message import *

def init_slash_commands_scheduled_event(params):
	
	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	@bot.slash_command(name="event")
	async def event(inter):
		pass

	@event.sub_command(name = "fetch")
	async def get_events_by_name(interaction, name):
		"""
		Get event by name
		Parameters
		----------
		name: Name of the event
		"""
		try:
			events = await interaction.guild.fetch_scheduled_events(with_user_count = True)
			events = list(filter(lambda event: (name.lower() in event.name.lower()), events))
			if len(events) == 0:
				msg = f'No event found with name : {name}'
			else:
				msg = f'Events found {len(events)} for `{name}`:'
				for e in events:
					end_time = f'{getTimeUtcPlusOne(e.scheduled_end_time, "%d %B %Y - %H:%M") if e.scheduled_end_time else "--"}'
					user_count = f'{e.user_count if e.user_count else 0}'
					msg += f'\n{e.id} / `{e.name}` in <#{e.channel.id}> / {getTimeUtcPlusOne(e.scheduled_start_time, "%d %B %Y - %H:%M")} ➜ {end_time} / {user_count} subs / by <@{e.creator_id}>'
					msg += '\n-------------------'
			await interaction.send(msg, ephemeral=True)
		except Exception as ex:
			print('----- /get_events_by_name() -----')
			print(ex)
			await log_exception(ex, '/get_events_by_name', interaction)


	@event.sub_command(name = "subscribers")
	async def event_subscribers(interaction, event_id, role: discord.Role = None):
		"""
		Get event subscribers
		Parameters
		----------
		event_id: ID of an exisitng event
		role: Role to assign
		"""
		try:
			guild = interaction.guild
			event = guild.get_scheduled_event(int(event_id))
			if event:
				users = await event.fetch_users().flatten()
				count = len(users)
				msg = f"Event : {event.name}\nSubscribers : {count}\n"
				assignedMembers = 0
				for member in users:
					try:
						msg += f'{member.mention} , '
						if role and (role not in member.roles):
							await member.add_roles(role)
							assignedMembers += 1
					except:
						print(member)
				if role: msg += f"\nAssigned role : {role.mention} / ({assignedMembers})"
			else: msg = "Event not found !!"
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /event_subscribers() -----')
			print(ex)
			await log_exception(ex, '/event_subscribers', interaction)
	
	
	flags = ["canceled", "completed", "active"]
	@event.sub_command(name = "edit-status")
	async def event_edit_status(interaction, event_id, flag=commands.Param(choices=flags), send_message : int = 0):
		"""
		Edit the even status
		Parameters
		----------
		event_id: Event ID
		flag: values canceled / completed / active
		"""
		try:
			if flag not in flags: 
				await interaction.send(f'⚠ Issue with the input (choose one of the provided options)', ephemeral=True)
			_status = {
				"canceled": discord.GuildScheduledEventStatus.canceled,
				"completed": discord.GuildScheduledEventStatus.completed,
				"active": discord.GuildScheduledEventStatus.active,
				"scheduled": discord.GuildScheduledEventStatus.scheduled,
			}
			event = await interaction.guild.fetch_scheduled_event(event_id = event_id)

			if flag == 'completed' and event.status == _status['scheduled']:
				await interaction.send("⚠ Cannot complete a non-started event", ephemeral=True)
				return
			if flag == 'canceled' and (event.status == _status['active'] or event.status == _status['completed']):
				await interaction.send("⚠ Cannot cancel an active or completed event.", ephemeral=True)
				return
			if event.status == _status[flag]: 
				await interaction.send('⚠ Status already edited', ephemeral=True)
				return
				
			if flag == 'active' and send_message:
				subscribers = await event.fetch_users().flatten()
				channel = bot.get_channel(textChannels['log-dms'])
				log_thread = await make_thread(channel, f"✉ DM/ ==▷ 🎭 / 👤")
				msg_dm = f"The event you subscribed to is :\n\n🔹 Live Now : **{event.name}**\nClick to join : {event.url}"
				log_thread = await send_bulk_dm(interaction, subscribers, log_thread, msg_dm)
				notifyMe = f'\n__Content__\n'
				await log_thread.send(notifyMe)
				await log_thread.send(msg_dm.strip())
				await log_thread.edit(archived=True)
			
			await event.edit(status = _status[flag])
			await interaction.send('Status Updated', ephemeral=True)
		except Exception as ex:
			print('----- /event_edit_status() -----')
			print(ex)
			await log_exception(ex, '/event_edit_status', interaction)

	
	@event.sub_command(name = "delete")
	async def event_delete_between_dates(interaction, name, from_date, to_date):
		"""
		Deleting events created with name between 2 dates
		Parameters
		----------
		name: Event name
		from_date: Start date to check after / example - 7/1/2022 21:15
		to_date: End date to check before / example - 7/30/2022 21:15
		"""
		try:
			tzinfo = timezone(timedelta(hours=1))
			from_date = dp.parse(from_date).replace(tzinfo=tzinfo)
			to_date = dp.parse(to_date).replace(tzinfo=tzinfo)
			if from_date >= to_date:
				await interaction.send('from_date < to_date !!', ephemeral=True)
				return

			await interaction.send(f'Deleting events created with name: __{name}__ between __{from_date.date()}__ & __{to_date.date()}__', ephemeral=True)
			
			guild = interaction.guild
			events_to_delete = filter(lambda event: (event.scheduled_start_time > from_date and event.scheduled_start_time < to_date and event.name == name), guild.scheduled_events)
			events_to_delete = list(events_to_delete)
			for event in events_to_delete:
				await event.delete()
			await interaction.send(f'Event(s) deleted : {len(events_to_delete)}', ephemeral=True)
		except Exception as ex:
			print('----- /event_delete_between_dates() -----')
			print(ex)
			await log_exception(ex, '/event_delete_between_dates', interaction)


	@event.sub_command(name = "create")
	async def event_create(interaction, name, channel:discord.VoiceChannel, scheduled_start_time, description=None, image_url=None, every_n_weeks:int=None, recurrence:int=None):
		"""
		Create scheduled event - \\n \\t /$
		Parameters
		----------
		name: Event name
		channel: Voice channel
		scheduled_start_time: Event's starting time / example - 7/23/2022 21:15
		description: Event's description - \\n \\t /$
		image_url: Cover image / example - http://teacode.ma/path/image.png
		every_n_weeks: Every week / 2 weeks -  1 <= every_n_weeks <= 4 (recurrence param should be set)
		recurrence: Number of (Weekly) events to create - 2 <= recurrence <= 5 (every_n_weeks param should be set)
		"""
		try:
			if (every_n_weeks and not recurrence) or (recurrence and not every_n_weeks):
				await interaction.send('*recurrence* and *every_n_weeks* should be set together !!', ephemeral=True)
				return
			
			if recurrence and (recurrence < appParams['recurrence_min'] or recurrence > appParams['recurrence_max']):
				await interaction.send(f"{appParams['recurrence_min']} <= *recurrence* <= {appParams['recurrence_max']} !!", ephemeral=True)
				return
			
			if every_n_weeks and (every_n_weeks < appParams['every_n_weeks_min'] or every_n_weeks > appParams['every_n_weeks_max']):
				await interaction.send(f"{appParams['every_n_weeks_min']} <= *every_n_weeks* <= {appParams['every_n_weeks_max']} !!", ephemeral=True)
				return

			count =  recurrence if recurrence else 1
			await interaction.send(f'Creating {count} event(s) in progress ...', ephemeral=True)
			
			guild = interaction.guild
			entity_type = discord.GuildScheduledEventEntityType.voice
			if description: description = replace_str(description, {"\\n": "\n", "\\t": "	", "/$": " "})

			image = None
			if image_url:
				response = requests.get(image_url)
				file_name = "event-cover.png"
				open(file_name, "wb").write(response.content)
				file = open(file_name, "rb")
				image = file.read()
				os.remove(file_name)

			start_time = dp.parse(scheduled_start_time)
			tzinfo = timezone(timedelta(hours=1))

			if recurrence and every_n_weeks:
				for i in range(recurrence):
					start_time = start_time.replace(tzinfo=tzinfo)
					await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel=channel, description=description, image=image)
					start_time = start_time + drel.relativedelta(weeks=every_n_weeks)
			else:
				start_time = start_time.replace(tzinfo=tzinfo)
				await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel=channel, description=description, image=image)

			await interaction.send(f'Created events : {count}', ephemeral=True)
		except Exception as ex:
			print('----- /event_create() -----')
			print(ex)
			await log_exception(ex, '/event_create', interaction)
