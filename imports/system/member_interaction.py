from setup.properties import *
from setup.actions import *

def init_member_interaction(params):

	bot = params['bot']
	discord = params['discord']


	######################## REPLY TO MSG ########################
	@bot.slash_command(name = "tc_emc", description="Edit message channel - \\n \\t /$")
	async def edit_msg_channel(interaction, content, msg_id, channel: discord.TextChannel, pin: int=0):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
			msg = await channel.fetch_message(int(msg_id))
			content = replace_str(content, {"\\n": "\n", "\\t": "	", "/$": " "})
			await msg.edit(content=content)
			if pin:
				await msg.pin()
			await interaction.send('Edit done', ephemeral=True)
		except Exception as ex:
			print('----- /edit_msg_channel() -----')
			print(ex)
			await log_exception(ex, '/edit_msg_channel', interaction)


	######################## REPLY TO MSG ########################
	@bot.slash_command(name = "tc_rc", description="Reply to msg channel - \\n \\t /$")
	async def reply_channel(interaction, reply, msg_id, channel: discord.TextChannel):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
			msg = await channel.fetch_message(int(msg_id))
			reply = replace_str(reply, {"\\n": "\n", "\\t": "	", "/$": " "})
			await msg.reply(reply)
			await interaction.send('Reply sent', ephemeral=True)
		except Exception as ex:
			print('----- /reply_channel() -----')
			print(ex)
			await log_exception(ex, '/reply_channel', interaction)


	######################## SEND MSG TO CHANNEL ########################
	@bot.slash_command(name = "tc_mc", description="Send msg to channel - \\n \\t /$")
	async def msg_channel(interaction, msg, channel: discord.TextChannel, pin: int=0):
		try:
			
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return

			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})
			msg = await channel.send(msg)
			if pin:
				await msg.pin()
			await interaction.send('Msg sent', ephemeral=True)
		
		except Exception as ex:
			print('----- /msg_channel() -----')
			print(ex)
			await log_exception(ex, '/msg_channel', interaction)

	######################## SEND MSG TO MEMBER ########################
	@bot.slash_command(name = "tc_mm", description="Send msg to member/role - \\n \\t /$")
	async def msg_member(interaction, msg, member: discord.Member = None, role: discord.Role = None):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return

			await interaction.send("Sending direct message...", ephemeral=True)
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})

			channel = bot.get_channel(textChannels['log-dms'])
			notifyMe = '──────────────────────'
			notifyMe += f'\nDM/ =▷'
			notifyMe += f'\n__To__'
			await channel.send(notifyMe)

			if role and member == None:
				pass
			elif role == None and member == None:
				member = interaction.author

			if role:
				members = role.members
				for m in members:
					try:
						_sentMsg = await send_msg(interaction, msg, m)
						notifyMe = '─────────────────'
						if _sentMsg:
							notifyMe += f'\nmessage ID : {_sentMsg.id}'
							notifyMe += f'\nchannel ID : {_sentMsg.channel.id}'
							notifyMe += f'\nMember: {m.mention} / {m.name}#{m.discriminator}'
						else: notifyMe += f'\nIssue with this member {m.mention} / {m.name}#{m.discriminator}'
						notifyMe += '\n--------------'
						await channel.send(notifyMe)
					except Exception as ex:
						print('----- /msg_member()/send_msg/role -----')
						print(ex)
						pass
				notifyMe = f'\nRole: **{role.mention}**'
				await channel.send(notifyMe)
			if member:
				_sentMsg = await send_msg(interaction, msg, member)
				notifyMe = '─────────────────'
				if _sentMsg:
					notifyMe += f'\nmessage ID : {_sentMsg.id}'
					notifyMe += f'\nchannel ID : {_sentMsg.channel.id}'
					notifyMe += f'\nMember: {member.mention} / {member.name}#{member.discriminator}'
				else: notifyMe += f'\nIssue with this member {member.mention} / {member.name}#{member.discriminator}'
				notifyMe += '\n--------------'
				await channel.send(notifyMe)

			notifyMe = f'\n__Content__\n'
			await channel.send(notifyMe)
			await channel.send(msg)

		except Exception as ex:
			print('----- /msg_member() -----')
			print(ex)
			await log_exception(ex, '/msg_member', interaction)

	######################## DELETE A MSG ########################
	@bot.slash_command(name = "tc_rm", description="Delete msg from public/private - ,")
	async def remove_msg_member(interaction, msg_ids, channel_id):
		try:
			if not is_founders(interaction):
				await interaction.send('❌ Missing Permissions')
				return
			await interaction.send("Deleting direct message...", ephemeral=True)
			msg_ids = msg_ids.split(',')
			_ch = await bot.fetch_channel(channel_id)
			for msg_id in msg_ids:
				try:
					msg = await _ch.fetch_message(msg_id)
					await msg.delete()
				except Exception as ex:
					print(msg_id)
					pass
		except Exception as ex:
			print('----- /remove_msg_member() -----')
			print(ex)
			await log_exception(ex, '/remove_msg_member', interaction)

	async def send_msg(interaction, message, member):
		try:
			channel = member.dm_channel
			if channel == None:
				channel = await member.create_dm()
			return await channel.send(message)
		except Exception as ex:
			print('----- send_msg() -----')
			print(ex)
			msg = f'Cannot send messages to {member.mention} / {member.name}#{member.discriminator}'
			await log_exception(ex, 'send_msg()', interaction, None, True, msg)
			return None
