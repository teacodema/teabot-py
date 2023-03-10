import random
from imports.actions.common import *
from imports.data_common.config import *
from imports.data_server.config import *

def init_temporary(params):
	
	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name="temp")
	async def temp(inter):
		pass

	# tags_roles = {
	# 	'frontend': [
	# 		"Gatsby", "jQuery", "Javascript",
	# 		"Bootstrap", "Tailwind Css", "Less", 
	# 		"Sass", "Html / Css", "Svelte",
	# 		"EmberJs", "ReactJs", "VueJs", 
	# 		"Angular", "Typescript",
	# 	],
	# 	'backend': [
	# 		"Ruby on Rails",
	# 		"Ruby","Flask","Django","Python",
	# 		"Spring","Spring Boot","Java", "DotNet",
	# 		"VB.Net","C#","CodeIgniter","Symfony","Laravel",
	# 		"Php","ExpressJs","NodeJs",
	# 		"Next JS", "Nest JS", "Nuxt JS"    
	# 	],
	# 	'devops': [
	# 		"Gradle", "Selenium", "SonarQube",
	# 		"Ansible","Jenkins","Kubernetes","Docker",
	# 	],
	# 	'database': [
	# 		"Neo4j", "RethinkDB", "Cassandra", "Firebase", "Redis",
	# 		"MongoDB","SQL Server","Oracle","SQLite","PostgreSQL","MySQL",
	# 		"GraphQL", "NoSQL", "Transact-SQL","PL / SQL", "SQL",
	# 	],
	# 	'mobile': [
	# 		"Xamarin Forms", "Xamarin Native", 
	# 		"iOS", "Android", "Ionic", "Flutter", 
	# 		"Dart", "React Native", "Kotlin"
	# 	],
	# 	'software': [
	# 		"Notepad++","Vim","CodeBlocks","Brackets",
	# 		"NetBeans","Eclipse","VSCode","Atom",
	# 		"Sublime Text","Visual Studio","Android Studio","DataGrip",
	# 		"RubyMine","Rider (.Net)","PyCharm","PhpStorm",
	# 		"WebStorm","IntelliJ IDEA",
	# 	],
	# 	'os-shells': [
	# 		"iTerm2", "Bash", "Cmder", "Windows Terminal",
	# 		"Mac", "Linux", "Windows",
	# 	],
	# 	'version-control': [
	# 		"Svn", "SourceTree", "Phabricator", "Git Kraken",
	# 		"Bitbucket", "GitLab", "Github", "Git",
	# 	]
	# }

	# @bot.slash_command(name = "roles-to-tags")
	# async def roles_to_tags(interaction, category:discord.CategoryChannel):
	# 	for fch in category.forum_channels:
	# 		tags = tags_roles[fch.name]
	# 		tags_to_add = []
	# 		for tagname in tags:
	# 			tag = discord.ForumTag(name = tagname)
	# 			tags_to_add.append(tag)
	# 		print(fch.name, len(tags_to_add))
	# 		await fch.edit(available_tags=tags_to_add)

	########## MATCH 2 MEMBERS ############
	@temp.sub_command(name = "make-pair")
	async def make_pair(interaction, role: discord.Role = None):
		try:
			voice = interaction.author.voice
			if (voice == None) and (role == None):
				await interaction.send('You need to choose a role or be connected to a voice channel', ephemeral=True)
				return
			if voice:
				members = list(voice.channel.members)
			elif role:
				members = role.members
			member1 = random.choice(members)
			members.remove(member1)
			member2 = random.choice(members)
			msg = f'Chosen members : {member1.mention} & {member2.mention}'
			await interaction.send(msg.strip())
		except Exception as ex:
			print('----- /make_pair() -----')
			print(ex)
			await log_exception(ex, '/make_pair', interaction)

	# @bot.event
	# async def on_guild_scheduled_event_update(before, after):
	# 	try:
	# 		invite = await after.channel.create_invite(max_age=appParams['inviteMaxAge'], max_uses=100, reason=f'Event Started Title : {after.name}')
	# 		event_invite_link = f'{invite}?event={after.id}'
	# 		if before.status != after.status:
	# 			channel = bot.get_channel(textChannels['general'])
	# 			guild = bot.get_guild(guildId)
	# 			if after.channel_id in voice_roles:
	# 				role = guild.get_role(voice_roles[after.channel_id])
	# 			else:
	# 				role = guild.get_role(roles['members'])
	# 			if after.status == discord.GuildScheduledEventStatus.active:
	# 				msg = f'🟢 Live : **{after.name}** / {role.mention}\nFeel free to join\n{event_invite_link}'
	# 				await channel.send(msg.strip())
	# 			elif after.status == discord.GuildScheduledEventStatus.completed:
	# 				msg = f'🟥 Event ended / {after.name}\nThank you for attending\nsee you soon 👋'
	# 				await channel.send(msg.strip())
	# 	except Exception as ex:
	# 		print('----- on_guild_scheduled_event_update(evt) -----')
	# 		print(ex)
	# 		await log_exception(ex, 'on_guild_scheduled_event_update(evt)', None, bot)


	@temp.sub_command(name = "category-channels-delete")
	async def category_channels_delete(interaction, category: discord.CategoryChannel, delete_channels:int = 0):
		msg_r = ''
		if delete_channels:
			msg_r = await remove_channels(category.channels);
		await category.delete()
		msg_r = f"Category deleted\n{msg_r}"
		await interaction.send(msg_r, ephemeral=True)
		
	
	@temp.sub_command(name = "channel-bulk-delete")
	async def channel_bulk_delete(interaction, channels):
		msg_r = await remove_channels(channels);
		await interaction.send(msg_r, ephemeral=True)


	async def remove_channels(channels):
		msg_r = 'Channels deleted'
		if isinstance(channels, str):
			channels = split_str(channels)
		msg_err = None
		for channel in channels:
			channel_name = '-----'
			try:
				if isinstance(channel, str):			
					channel = channel.replace('<#', '').replace('>', '')
					channel = bot.get_channel(int(channel))
				if channel:
					channel_name = channel.name
					await channel.delete()
				else: msg_err += f'\nChannel do not exist'
			except Exception as ex:
				print(str(ex))
				msg_err += f'\n{channel_name} Not deleted'
		if msg_err: msg_r += f'\nExcept : \n{msg_err}'
		return msg_r