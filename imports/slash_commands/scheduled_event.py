import requests, os
import dateutil.parser as dp
import dateutil.relativedelta as drel
from datetime import timedelta, timezone
from setup.data.params import *
from setup.actions.common import *

def init_slash_commands_scheduled_event(params):
	
	bot = params['bot']
	discord = params['discord']
	inspect = params['inspect']

	@bot.slash_command(name = "subscribers")
	async def event_subscribers(interaction, event_id, role: discord.Role = None):
		"""
		Get event subscribers
		Parameters
		----------
		event_id: ID of an exisitng event
		role: Role to assign
		"""
		try:
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			await interaction.send("Loading...", ephemeral=True)
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
	
	@bot.slash_command(name = "event-delete-between-dates")
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
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
			tzinfo = timezone(timedelta(hours=1))
			from_date = dp.parse(from_date).replace(tzinfo=tzinfo)
			to_date = dp.parse(to_date).replace(tzinfo=tzinfo)
			if from_date >= to_date:
				await interaction.send('from_date < to_date !!', ephemeral=True)
				return

			await interaction.send(f'Deleting events created with name: __{name}__ between __{from_date.date()}__ & __{to_date.date()}__')
			
			guild = interaction.guild
			events_to_delete = filter(lambda event: (event.scheduled_start_time > from_date and event.scheduled_start_time < to_date and event.name == name), guild.scheduled_events)
			events_to_delete = list(events_to_delete)
			for event in events_to_delete:
				await event.delete()
			await interaction.send(f'Event(s) deleted : {len(events_to_delete)}')
		except Exception as ex:
			print('----- /event_delete_between_dates() -----')
			print(ex)
			await log_exception(ex, '/event_delete_between_dates', interaction)


	@bot.slash_command(name = "event-create")
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
			
			action_name = inspect.stack()[0][3]
			if not is_allowed(interaction, action_name):
				await interaction.send('❌ Missing Permissions', ephemeral=True)
				return
				
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
			await interaction.send(f'Creating {count} event(s) in progress ...')
			
			guild = interaction.guild
			channel_id = channel.id
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
					await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel_id=channel_id, description=description, image=image)
					start_time = start_time + drel.relativedelta(weeks=every_n_weeks)
			else:
				start_time = start_time.replace(tzinfo=tzinfo)
				await guild.create_scheduled_event(name=name, scheduled_start_time=start_time, entity_type=entity_type, channel_id=channel_id, description=description, image=image)

			await interaction.send(f'Created events : {count}')
		except Exception as ex:
			print('----- /event_create() -----')
			print(ex)
			await log_exception(ex, '/event_create', interaction)
