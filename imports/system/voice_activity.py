from setup.properties import *
from setup.actions import *

def init_voice_activity(params):
	
	bot = params['bot']
	tasks = params['tasks']

	async def logVoice(guild, member, voice, joining, role_toggle_fct, voice1 = None, voice2 = None):
		if voice.channel and voice_data.__contains__(voice.channel.category_id):
			category = voice_data[voice.channel.category_id]
			if category.__contains__('vc-role'):
				role = guild.get_role(category['vc-role'])
				await role_toggle_fct(role)
			channel = bot.get_channel(category['vc-text'])
			if joining:
				msg = f'<:userjoin:902613054544560149> {member.mention} joined __**{voice.channel.name}**__'
				if (not voice1.channel and voice2.channel) or (voice1.channel and voice2.channel and voice1.channel.category_id != voice2.channel.category_id):
					if member.voice and member.voice.self_deaf:
						msg += f"\n_{member.display_name}_ won't be able to hear you now 🔇"
			else:
				msg = f'<:userleft:902612227662684170> {member.mention} left __**{voice.channel.name}**__'
			task_send_msg(channel, msg) # await channel.send(msg)

	async def check_deafen(member, voice1, voice2):
		if voice2.channel and voice_data.__contains__(voice2.channel.category_id):
			if voice1.channel and voice2.channel:
				if voice1.self_deaf != voice2.self_deaf:
					if not voice2.self_deaf:
						msg = f"_{member.display_name}_ is able to hear you now 🔉"
					elif voice2.self_deaf:
						msg = f"_{member.display_name}_ won't be able to hear you now 🔇"
					category = voice_data[voice2.channel.category_id]
					channel = bot.get_channel(category['vc-text'])
					await channel.send(msg)

					
	######################## VOICE ########################
	@bot.event
	async def on_voice_state_update(member, voice1, voice2):
		try:
			await check_deafen(member, voice1, voice2)
			if (voice1 and voice2) and (voice1.channel and voice2.channel) and (voice1.channel.id == voice2.channel.id):
				return
			guild = bot.get_guild(guildId)
			if voice1 and voice1.channel:
				await logVoice(guild, member, voice1, False, member.remove_roles)
			if voice2 and voice2.channel:
				await logVoice(guild, member, voice2, True, member.add_roles, voice1, voice2)

			# voice_state = member.guild.voice_client
			# if voice_state and len(voice_state.channel.members) == 1:
			# 	await voice_state.disconnect()
		except Exception as ex:
			print('----- on_voice_state_update(evt) -----')
			print(ex)
			await log_exception(ex, 'on_voice_state_update(evt)', None, bot)


	def task_send_msg(channel, msg):
		@tasks.loop(seconds=2, count=2, reconnect=False)
		async def send_msg():
			if send_msg.current_loop == 0:
				return
			await channel.send(msg)
		send_msg.start()