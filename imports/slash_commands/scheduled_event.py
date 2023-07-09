import requests, os
import dateutil.parser as dp
import dateutil.relativedelta as drel
from datetime import timedelta, timezone
from imports.data_common.config import *
from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.message import *

def init_slash_commands_scheduled_event(params):
	
	bot = params['bot']
	discord = params['discord']
	commands = params['commands']
	_status = {
		"canceled": discord.GuildScheduledEventStatus.canceled,
		"completed": discord.GuildScheduledEventStatus.completed,
		"active": discord.GuildScheduledEventStatus.active,
		"scheduled": discord.GuildScheduledEventStatus.scheduled,
	}

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
				msg = f'Events found for `{name}`: {len(events)}'
				for e in events:
					end_time = f'{getTimeUtcPlusOne(e.scheduled_end_time, "%d %B %Y - %H:%M") if e.scheduled_end_time else "--"}'
					user_count = f'{e.user_count if e.user_count else 0}'
					msg += f'\n\tEvent : {e.id} / `{e.name}` in <#{e.channel_id}>'
					msg += f'\n\tDateTime : {getTimeUtcPlusOne(e.scheduled_start_time, "%d %B %Y - %H:%M")} ➜ {end_time}'
					msg += f'\n\tSubscribers : {user_count} subs / by <@{e.creator_id}>'
					event_status = {i for i in _status if _status[i]==e.status}.pop()
					msg += f'\n\tStatus : {event_status}'
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
			if event == None:
				await interaction.send("⚠ Event not found !!", ephemeral=True)
				return
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
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /event_subscribers() -----')
			print(ex)
			await log_exception(ex, '/event_subscribers', interaction)
	
	
	flags = ["canceled", "completed", "active"]
	@event.sub_command(name = "update-status")
	async def event_edit_status(interaction, event_id, flag=commands.Param(choices=flags), send_message : int = 0, announcement_channel : discord.abc.GuildChannel = None):
		"""
		Edit the even status
		Parameters
		----------
		event_id: Event ID
		flag: values canceled / completed / active
		send_message: send dm to subscribers when event is Live
		announcement_channel: Channel where to Notify the community
		"""
		try:
			log_thread = None
			if flag not in flags: 
				await interaction.send(f'⚠ Issue with the input (choose one of the provided options)', ephemeral=True)
			event = await interaction.guild.fetch_scheduled_event(event_id = event_id)

			if event == None:
				await interaction.send("⚠ Event not found !!", ephemeral=True)
				return
			if flag == 'completed' and event.status == _status['scheduled']:
				await interaction.send("⚠ Cannot complete a non-started event", ephemeral=True)
				return
			if flag == 'canceled' and (event.status == _status['active'] or event.status == _status['completed']):
				await interaction.send("⚠ Cannot cancel an active or completed event.", ephemeral=True)
				return
			if event.status == _status[flag]: 
				await interaction.send('⚠ Status already edited', ephemeral=True)
				return
				
			if flag == 'active':
				msg_dm = f"🔹 Live Now : **{event.name}**\nClick to join : {event.url}"
				if send_message:
					subscribers = await event.fetch_users().flatten()
					channel = bot.get_channel(textChannels['log-dms'])
					log_thread = await make_thread(channel, f"✉ DM/ ==▷ 🎭 / 👤")
					log_thread = await send_bulk_dm(interaction, subscribers, log_thread, msg_dm)
					notifyMe = f'\n__Content__\n'
					await log_thread.send(notifyMe)
					await log_thread.send(msg_dm.strip())
					await log_thread.edit(archived=True)
				if announcement_channel:
					if event.channel_id in voice_roles:
						role = interaction.guild.get_role(voice_roles[event.channel_id])
						msg_dm += f'\n<@&{role.id}>'
					await announcement_channel.send(msg_dm.strip())
			
			if flag == 'completed' and announcement_channel:
				msg = f'🔸 Event ended : **{event.name}**\nThank you for attending\nsee you soon 👋'
				await announcement_channel.send(msg.strip())
			
			await event.edit(status = _status[flag])
			await interaction.send('Status Updated', ephemeral=True)
		except Exception as ex:
			if log_thread: await log_thread.edit(archived=True)
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
	async def event_create(interaction, name, channel:discord.VoiceChannel, scheduled_start_time, description=None, image_url=None, recurrence=commands.Param(choices=recurrence_values), recurrence_number:int=None, how_many:int=None, event_id=None):
		"""
		Create scheduled event - \\n \\t /$
		Parameters
		----------
		name: Event name
		channel: Voice channel
		scheduled_start_time: Event's starting time / example - 7/23/2022 21:15
		description: Event's description - \\n \\t /$
		image_url: Cover image / example - http://teacode.ma/path/image.png
		recurrence: Every week/day -  1 <= recurrence <= 4 (how_many param should be set)
		recurrence_number: Example : Every 2 or 3 days/weeks
		how_many: Number of (weekly/daily) events to create - 2 <= how_many <= 5 (recurrence param should be set)
		event_id: ID of an exisitng event (duplicate event)
		"""
		try:
			event = None
			if event_id:
				event = await interaction.guild.fetch_scheduled_event(event_id = event_id)
				if event == None:
					await interaction.send("⚠ Event not found !!", ephemeral=True)
					return

			if (how_many and not (recurrence and recurrence_number)) or ((recurrence and recurrence_number) and not how_many):
				await interaction.send('*recurrence*, *recurrence_number* and *how_many* should be set together !!', ephemeral=True)
				return

			if recurrence != "None":
				if recurrence_number and (recurrence_number < appParams['recurrence_min'] or recurrence_number > appParams['recurrence_max']):
					await interaction.send(f"{appParams['recurrence_min']} <= *recurrence_number* <= {appParams['recurrence_max']} !!", ephemeral=True)
					return
			
			if how_many and (how_many < appParams['how_many_min'] or how_many > appParams['how_many_max']):
				await interaction.send(f"{appParams['how_many_min']} <= *how_many* <= {appParams['how_many_max']} !!", ephemeral=True)
				return

			count =  how_many if how_many else 1
			await interaction.send(f'Creating {count} event(s) in progress ...', ephemeral=True)
			
			guild = interaction.guild
			entity_type = discord.GuildScheduledEventEntityType.voice
			if description: description = replace_str(description, {"\\n": "\n", "\\t": "	", "/$": " "})
			elif event: description = event.description

			image = None
			if image_url:
				response = requests.get(image_url)
				file_name = "event-cover.png"
				open(file_name, "wb").write(response.content)
				file = open(file_name, "rb")
				image = file.read()
				os.remove(file_name)
			elif event: image = event.image

			tzinfo = timezone(timedelta(hours=0))
			start_time = dp.parse(scheduled_start_time)

			if how_many and recurrence != "None":
				for i in range(how_many):
					start_time = start_time.replace(tzinfo=tzinfo)
					await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel=channel, description=description, image=image)
					if recurrence == "weekly":
						start_time = start_time + drel.relativedelta(weeks=recurrence_number)
					elif recurrence == "daily":
						start_time = start_time + drel.relativedelta(days=recurrence_number)
			else:
				start_time = start_time.replace(tzinfo=tzinfo)
				await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel=channel, description=description, image=image)

			await interaction.send(f'Created events : {count}', ephemeral=True)
		except Exception as ex:
			print('----- /event_create() -----')
			print(ex)
			await log_exception(ex, '/event_create', interaction)


	@event.sub_command(name = "update")
	async def event_update(interaction, name, new_name=None, new_start_time=None, channel:discord.VoiceChannel=None, description=None, image_url=None):
		"""
		Create scheduled event - \\n \\t /$
		Parameters
		----------
		name: Search term / Event name
		new_name: New name for event(s)
		new_start_time: Event's new starting time / example - 15:15
		channel: Voice channel
		description: Event's description - \\n \\t /$
		image_url: Cover image / example - http://teacode.ma/path/image.png
		"""
		try:
			params = interaction.filled_options
			new_data_exists = False
			for p in params:
				if p != "name" and params[p] != None:
					new_data_exists = True
					break;
			if not new_data_exists:
				await interaction.send("No new data provided to update !!")
				return
			guild = interaction.guild
			events_to_update = list(filter(lambda event: event.name == name, guild.scheduled_events))
			if len(events_to_update) == 0:
				await interaction.send(f"No event(s) found with name `{name}` !!")
				return
			image = None
			if image_url:
				response = requests.get(image_url)
				file_name = "event-cover.png"
				open(file_name, "wb").write(response.content)
				file = open(file_name, "rb")
				image = file.read()
				os.remove(file_name)

			count = 0
			tzinfo = timezone(timedelta(hours=0))
			for event in events_to_update:
				try:
					if new_name == None: new_name = event.name
					if description:
						description = replace_str(description, {"\\n": "\n", "\\t": "	", "/$": " "})
					else:
						description = event.description
					if image == None: image = event.image
					if channel == None: channel = event.channel
					if new_start_time == None:
						start_time = event.scheduled_start_time
					else:
						start_time = dp.parse(f'{event.scheduled_start_time.date()} {new_start_time}')
						start_time = start_time.replace(tzinfo=tzinfo)
					await event.edit(name=new_name, scheduled_start_time=start_time, description=description, image=image, channel=channel)
					count += 1
				except Exception as ex:
					print(ex, event.id)
					await interaction.send(f"Issue with event ID : {event.id}\n", ephemeral=True)
					pass
			
			await interaction.send(f'Updated events : {count}', ephemeral=True)
		except Exception as ex:
			print('----- /event_update() -----')
			print(ex)
			await log_exception(ex, '/event_update', interaction)
