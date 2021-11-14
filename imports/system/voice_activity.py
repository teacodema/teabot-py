from setup.properties import *
from setup.actions import *

def init_voice_activity(params):
	
	bot = params['bot']
	get = params['get']

	######################## VOICE ########################
	@bot.event
	async def on_voice_state_update(member, voice1, voice2):
		try:
			await showVoiceChat(member, voice1, voice2, bot, get)
			await showHelpVoice(member, voice1, voice2, bot, get)
			await logActivity(member, voice1, voice2, bot, get)
			await logStaffVoice(member, voice1, voice2, bot, get)
			await logModeratorsVoice(member, voice1, voice2, bot, get)
			await logAllVoice(member, voice1, voice2, bot, get)
			
			await showLTVoice(member, voice1, voice2, bot, get)
			# voice_state = member.guild.voice_client
			# if voice_state and len(voice_state.channel.members) == 1:
			# 	await voice_state.disconnect()
		except Exception as ex:
			print('----- on_voice_state_update -----')
			print(ex)

	######################## LOG VOICE #Voice Channels ########################
	async def logActivity(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'activities-notes', 'activities')
		except Exception as ex:
			print('----- logActivity -----')
			print(ex)


	######################## LOG VOICE #Help › Voice ########################
	async def showHelpVoice(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'help-chat', 'help-voice', 'help-room')
			helpVoiceCategoryID = categories['help-voice']
			if (voice2.channel and voice2.channel.category_id == helpVoiceCategoryID):
				channels = voice2.channel.category.voice_channels
				noEmptyChannel = True
				for ch in channels:
					if len(ch.members) == 0:
						noEmptyChannel = False
						break
				if noEmptyChannel:
					vc = channels[0]
					vc_name = vc.name
					index = len(channels) + 1
					await voice2.channel.clone(name=f'{vc_name} #{index}')		
			# DELETE CHANNEL IF EMPTY AND LEAVE FIRST ONE
			if (voice1.channel and voice1.channel.category_id == helpVoiceCategoryID):
				channels = voice1.channel.category.voice_channels
				helpRoom1 = channels.pop(0)
				emptyChannels = [] # Store empty channels
				for ch in channels:
					if len(ch.members) == 0:
						emptyChannels.append(ch)
				if len(helpRoom1.members) != 0:
					helpRoom2 = emptyChannels.pop(0)
				try:
					for ch in emptyChannels:
						await ch.delete()
				except Exception as ex:
					print(ex)
		except Exception as ex:
			print('----- showHelpVoice -----')
			print(ex)


	######################## LOG VOICE #Voice Channels ########################
	async def showVoiceChat(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'voice-chat', 'voice-channels', 'voice-room')
		except Exception as ex:
			print('----- showVoiceChat -----')
			print(ex)


	######################## LOG VOICE #Voice Channels ########################
	async def logStaffVoice(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'staff-notes', 'staff-corner')
		except Exception as ex:
			print('----- logStaffVoice -----')
			print(ex)


	async def logModeratorsVoice(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'moderators-notes', 'moderators-corner')
		except Exception as ex:
			print('----- logStaffVoice -----')
			print(ex)


	######################## LOG ALL VOICE ########################
	async def logAllVoice(member, voice1, voice2, bot, get):
		try:
			logChannel = bot.get_channel(textChannels['log-voice'])
			msg = getVoiceLogMessage(member, voice1, voice2)

			if (not voice1.channel and voice2.channel):
				await logChannel.send(msg)
			elif (voice1.channel and not voice2.channel):
				await logChannel.send(msg)
			elif (voice1.channel.id != voice2.channel.id):
				await logChannel.send(msg)

		except Exception as ex:
			print('----- logAllVoice -----')
			print(ex)
	
	
	async def logVoice(member, voice1, voice2, channelID, categoryID, roleID = None):
		guild = bot.get_guild(guildId)
		categoryID = categories[categoryID]
		logChannel = bot.get_channel(textChannels[channelID])
		role = None
		if roleID:
			role = get(guild.roles, id = roles[roleID])
		msg = getVoiceLogMessage(member, voice1, voice2)
		if (not voice1.channel and voice2.channel):
			if (voice2.channel.category_id == categoryID):
				await logChannel.send(msg)
				if (role): await member.add_roles(role)
		elif (voice1.channel and not voice2.channel):
			if (voice1.channel.category_id == categoryID):
				await logChannel.send(msg)
				if (role): await member.remove_roles(role)
		elif (voice1.channel.id != voice2.channel.id):
			if (voice2.channel.category_id == categoryID):
				await logChannel.send(msg)
				if (role): await member.add_roles(role)
			else:
				if (role): await member.remove_roles(role)

	
	def getVoiceLogMessage(member, voice1, voice2):
		try:
			if voice1.channel:
				icon = '<:userleft:902612227662684170>'
				msg = f'{icon} {member.mention} left __**{voice1.channel.name}**__'
			if voice2.channel:
				icon = '<:userjoin:902613054544560149>'
				msg = f'{icon} {member.mention} joined __**{voice2.channel.name}**__'
			return msg
		except Exception as ex:
			print('----- getVoiceLogMessage -----')
			print(ex)
			return ""


	######################## LOG VOICE #Help › Voice ########################
	async def showLTVoice(member, voice1, voice2, bot, get):
		try:
			# await logVoice(member, voice1, voice2, 'help-chat', 'help-voice', 'help-room')
			helpVoiceCategoryID = 909513881842515990 # Learn Together
			if (voice2.channel and voice2.channel.category_id == helpVoiceCategoryID):
				channels = voice2.channel.category.voice_channels
				noEmptyChannel = True
				for ch in channels:
					if len(ch.members) == 0:
						noEmptyChannel = False
						break
				if noEmptyChannel:
					vc = channels[0]
					vc_name = vc.name
					index = len(channels) + 1
					await voice2.channel.clone(name=f'{vc_name} #{index}')		
			# DELETE CHANNEL IF EMPTY AND LEAVE FIRST ONE
			if (voice1.channel and voice1.channel.category_id == helpVoiceCategoryID):
				channels = voice1.channel.category.voice_channels
				helpRoom1 = channels.pop(0)
				emptyChannels = [] # Store empty channels
				for ch in channels:
					if len(ch.members) == 0:
						emptyChannels.append(ch)
				if len(helpRoom1.members) != 0:
					helpRoom2 = emptyChannels.pop(0)
				try:
					for ch in emptyChannels:
						await ch.delete()
				except Exception as ex:
					print(ex)
		except Exception as ex:
			print('----- showHelpVoice -----')
			print(ex)