import random
from imports.data_server.config import *
from imports.actions.common import *
from imports.actions.member import *

def init_slash_commands_member(params):
	
	bot = params['bot']
	discord = params['discord']	
	commands = params['commands']

	@bot.slash_command(name="member")
	async def member(inter):
		pass

	######################## WELCOME MEMBER CMD ########################
	@member.sub_command(name = "welcome")
	async def tc_welcome(interaction, member: discord.Member, assign_role: int=0, send_dm: int=0, append_event_to_dm: int=0, use_webhook: int=0):
		"""
		Welcome users manually (dm + assign initial roles)
		Parameters
		----------
		member: Server existing member
		assign_role: Assign initial roles - enter 1 to activate (default 0)
		send_dm: Send a dm - enter 1 to activate (default 0)
		append_event_to_dm: Add message for next event if exists (default 0)
		use_webhook: Make a webhook for the new member - enter 1 to activate (default 0)
		"""
		try:
			msg = await welcomeMember(params, member, assign_role, send_dm, append_event_to_dm, use_webhook)
			channel = bot.get_channel(textChannels['log-server'])			
			await channel.send(msg.strip())
		except Exception as ex:
			print('----- /tc_welcome() -----')
			print(ex)
			await log_exception(ex, '/tc_welcome', interaction)


	######### PICK RANDOM USER #######
	@member.sub_command(name = "pick-speaker", description = "Choose a random speaker - (events only !!)")
	async def pick_speaker(interaction):
		try:
			voice = interaction.author.voice
			if voice:
				members = voice.channel.members
				members = list(filter(is_not_host_or_bot, members))
				if len(members) == 0:
					msg = 'No member chosen !! - Reasons'
					msg+= '\n- No members available in the voice channel'
					msg+= '\n- Only hosts/bot are connected for now'
					await interaction.send(msg.strip(), ephemeral=True)
					return

				member = random.choice(members)
				msg = f'Chosen member : {member.mention}'
			else:
				msg = '⚠ No busy voice channel'
			await interaction.send(msg.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /pick_speaker() -----')
			print(ex)
			await log_exception(ex, '/pick_speaker', interaction)


	####################### MAKE A WEBHOOK #######################
	@member.sub_command(name = "make-webhook")
	async def tc_make_webhook(interaction, member: discord.Member, channel: discord.abc.GuildChannel, msg, name=None):
		"""
		Make a webhook - \\n \\t /$
		Parameters
		----------
		member: Server existing member
		msg: Message to send by the webhook - \\n \\t /$
		channel: Channel where to send the msg
		name: Webhook name
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			if name == None:
				name = member.display_name
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})
			webhook = await channel.create_webhook(name=name)
			await webhook.send(f'{msg}', username=name, avatar_url=member.display_avatar.url)
			await webhook.delete()
			await interaction.send('✅ Webhook made', ephemeral=True)
		except Exception as ex:
			await interaction.send('❌ Webhook not made', ephemeral=True)
			print('----- /tc_make_webhook() -----')
			print(ex)
			await log_exception(ex, '/tc_make_webhook', interaction)
	