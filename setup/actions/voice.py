from setup.data.params import *

async def logVoice(params, guild, member, voice, joining, role_toggle_fct, voice1 = None, voice2 = None):
	bot = params['bot']
	if voice.channel and voice_data.__contains__(voice.channel.category_id):
		category = voice_data[voice.channel.category_id]
		if category.__contains__('vc-role'):
			role = guild.get_role(category['vc-role'])
			await role_toggle_fct(role)
		channel = bot.get_channel(category['vc-text'])
		if joining:
			msg = f'{emojis["userjoin"]} {member.mention} joined __**{voice.channel.name}**__'
			if (not voice1.channel and voice2.channel) or (voice1.channel and voice2.channel and voice1.channel.category_id != voice2.channel.category_id):
				if member.voice and member.voice.self_deaf:
					msg += f"\n**{member.display_name}** : I won't be able to hear you 🔇"
		else:
			msg = f'{emojis["userleft"]} {member.mention} left __**{voice.channel.name}**__'
		task_send_msg(params, channel, msg) # await channel.send(msg)

async def check_deafen(params, member, voice1, voice2):
	bot = params['bot']
	if voice2.channel and voice_data.__contains__(voice2.channel.category_id):
		if voice1.channel and voice2.channel:
			if voice1.self_deaf != voice2.self_deaf:
				if not voice2.self_deaf:
					msg = f"**{member.display_name}** : I'm able to hear you 🔉"
				elif voice2.self_deaf:
					msg = f"**{member.display_name}** : I won't be able to hear you 🔇"
				category = voice_data[voice2.channel.category_id]
				channel = bot.get_channel(category['vc-text'])
				await channel.send(msg)

def task_send_msg(params, channel, msg):
	tasks = params['tasks']
	@tasks.loop(seconds=2, count=2, reconnect=False)
	async def send_msg():
		if send_msg.current_loop == 0:
			return
		await channel.send(msg)
	send_msg.start()