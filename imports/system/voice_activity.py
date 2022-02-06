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
			# await logModeratorsVoice(member, voice1, voice2, bot, get)
			await logAllVoice(member, voice1, voice2, bot, get)
			
			# voice_state = member.guild.voice_client
			# if voice_state and len(voice_state.channel.members) == 1:
			# 	await voice_state.disconnect()
		except Exception as ex:
			print('----- on_voice_state_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_voice_state_update(evt)', None, bot)


	######################## LOG VOICE #Help › Voice ########################
	async def showHelpVoice(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'help-chat', 'help-voice', 'help-room')
			# await duplicateVC(categories['help-voice'], voice1, voice2, bot)
		except Exception as ex:
			print('----- showHelpVoice() -----')
			print(ex)
			await log_exception(ex, 'showHelpVoice()', None, bot)


	######################## LOG VOICE #Voice Channels ########################
	async def showVoiceChat(member, voice1, voice2, bot, get):
		try:
			await logVoice(member, voice1, voice2, 'voice-chat', 'voice-channels', 'voice-room')
		except Exception as ex:
			print('----- showVoiceChat() -----')
			print(ex)
			await log_exception(ex, 'showVoiceChat()', None, bot)


	# async def logModeratorsVoice(member, voice1, voice2, bot, get):
	# 	try:
	# 		await logVoice(member, voice1, voice2, 'moderators-notes', 'moderators-corner')
	# 	except Exception as ex:
	# 		print('----- logModeratorsVoice() -----')
	# 		print(ex)
	# 		await log_exception(ex, 'logModeratorsVoice()', None, bot)


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
			print('----- logAllVoice() -----')
			print(ex)
			await log_exception(ex, 'logAllVoice()', None, bot)
	
	
	async def logVoice(member, voice1, voice2, channelID, categoryID, roleID = None):
		try:
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
		except Exception as ex:
			print('----- logVoice() -----')
			print(ex)
			await log_exception(ex, 'logVoice()', None, bot)

	
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
			print('----- getVoiceLogMessage() -----')
			print(ex)
			return ""


	async def duplicateVC(categoryID, voice1, voice2, bot):
		if (voice2.channel and voice2.channel.category_id == categoryID):
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
		if (voice1.channel and voice1.channel.category_id == categoryID):
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