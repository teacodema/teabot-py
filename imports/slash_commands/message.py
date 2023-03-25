from imports.actions.common import *
from imports.actions.message import *

def init_slash_commands_message(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	@bot.slash_command(name="message")
	async def message(inter):
		pass

	@message.sub_command(name = "poll")
	async def poll(interaction, header, options, emojis, channel:discord.TextChannel = None):
		"""
		Make a poll
		Parameters
		----------
		header: Header message (part I)
		options: Options of the poll separated by $$ (part II)
		emojis: Emojis for the users
		channel: Target channel
		"""
		try:
			if channel == None: channel = interaction.channel
			msg = f'{header}\n'
			emojis = split_str(emojis)
			options = split_str(options, '\$\$')
			index = 0
			for o in options:
				msg += f'\n{emojis[index]} - {o.strip()}'
				index += 1
			msg += '\n\n─────────────────────────'
			msg = await channel.send(msg.strip())
			for e in emojis:
				await msg.add_reaction(e)
		except Exception as ex:
			print('----- /poll() -----')
			print(ex)
			await log_exception(ex, '/poll', interaction)

	######################## PURGE ########################
	@message.sub_command(name = "purge")
	async def purge(interaction, limit: int=None, include_pin:int=None):
		"""
		Clear all messages
		Parameters
		----------
		limit: Optional for specific channels / limit <= 500
		include_pin: Include pinned messages
		"""
		try:
			channelsToClear = [
				textChannels['voice-chat'],
				textChannels['help-chat']
			]
			if not limit and interaction.channel.id not in channelsToClear:
				await interaction.send('❌ Wrong Target Channel', ephemeral=True)
				return

			if limit:
				if limit > 500:
					await interaction.send('You cannot delete more than 500 messages', ephemeral=True)
					return
				else:
					await interaction.send('Clearing messages ...', ephemeral=True)
					if include_pin: deletedMsgs = await interaction.channel.purge(limit = limit, bulk = True)
					else: deletedMsgs = await interaction.channel.purge(limit = limit, check = isNotPinned, bulk = True)
					await interaction.send(f'{len(deletedMsgs)} message(s) cleared', ephemeral=True)
					count = len(deletedMsgs)
					deletedMsgs.reverse()
					if count:
						await logPurgedMessages(params, interaction, count, deletedMsgs)
				return

			MAX_TO_DELETE = 500
			await interaction.send('Clearing everything ...', ephemeral=True)
			#await deleteMsg(params, purgedMsgs, interaction, MAX_TO_DELETE)
			deletedMsgs = await deleteMsg(params, interaction, MAX_TO_DELETE, include_pin)
			await interaction.send(f'{len(deletedMsgs)} message(s) cleared', ephemeral=True)
			count = len(deletedMsgs)
			# deletedMsgs.reverse()
			deletedMsgs = sorted(deletedMsgs, key=lambda msg: msg.created_at)
			if count:
				await logPurgedMessages(params, interaction, count, deletedMsgs)
			
		except Exception as ex:
			print('----- /purge() -----')
			print(ex)
			await log_exception(ex, '/purge', interaction)

	######################## REPLY TO MSG ########################
	@message.sub_command(name = "edit")
	async def tc_edit_msg_channel(interaction, content, msg_id, channel: discord.abc.GuildChannel, pin: int=0):
		"""
		Edit message channel - \\n \\t /$
		Parameters
		----------
		content: New message content - \\n \\t /$
		msg_id: Message ID to edit
		channel: Channel where to fetch the message by msg_id
		pin: Add to pinned channel messages - enter 1 to activate (default 0)
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			msg = await channel.fetch_message(int(msg_id))
			content = replace_str(content, {"\\n": "\n", "\\t": "	", "/$": " "})
			await msg.edit(content=content)
			if pin:
				await msg.pin()
			await interaction.send('Edit done', ephemeral=True)
		except Exception as ex:
			print('----- /tc_edit_msg_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_edit_msg_channel', interaction)


	######################## REPLY TO MSG ########################
	@message.sub_command(name = "reply")
	async def tc_reply_channel(interaction, reply, msg_id, channel: discord.abc.GuildChannel):
		"""
		Reply to msg channel - \\n \\t /$
		Parameters
		----------
		reply: Message content - \\n \\t /$
		msg_id: Message ID to reply to
		channel: Channel where to fetch the message by msg_id
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			msg = await channel.fetch_message(int(msg_id))
			reply = replace_str(reply, {"\\n": "\n", "\\t": "	", "/$": " "})
			await msg.reply(reply)
			await interaction.send('Reply sent', ephemeral=True)
		except Exception as ex:
			print('----- /tc_reply_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_reply_channel', interaction)


	######################## SEND MSG TO CHANNEL ########################
	@message.sub_command(name = "channel")
	async def tc_msg_channel(interaction, msg, channel: discord.abc.GuildChannel, pin: int=0):
		"""
		Send msg to channel - \\n \\t /$
		Parameters
		----------
		msg: Message content - \\n \\t /$
		channel: Channel where to send the message
		pin: Add to pinned channel messages - enter 1 to activate (default 0)
		"""
		try:
			if channel.category == None:
				await interaction.send('This is probably a category ⚠', ephemeral=True)
				return
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})
			msg = await channel.send(msg.strip())
			if pin:
				await msg.pin()
			await interaction.send('Msg sent', ephemeral=True)
		
		except Exception as ex:
			print('----- /tc_msg_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_msg_channel', interaction)

	######################## SEND MSG TO MEMBER ########################
	@message.sub_command(name = "member")
	async def tc_msg_member(interaction, msg, member: discord.Member = None, role: discord.Role = None, members = None):
		"""
		Send msg to member/role - \\n \\t /$
		Parameters
		----------
		msg: Message content - \\n \\t /$
		member: Server existing member
		role: Role members
		members: Server existing members separated by , or space
		"""
		try:
			msg = replace_str(msg, {"\\n": "\n", "\\t": "	", "/$": " "})

			if role == None and member == None and members == None:
				member = interaction.author

			channel = bot.get_channel(textChannels['log-dms'])
			log_thread = await make_thread(channel, f"✉ DM/ ==▷ 🎭 / 👤")
			
			target_members = []
			if members:
				members = split_str(members)
				for m in members:
					try:
						m = m.replace('<@!', '').replace('<@', '').replace('>', '')
						m = await interaction.guild.fetch_member(m)
						target_members.append(m)
					except Exception as ex:
						print(ex)
						pass

			if member:
				target_members.append(member)
			if role:
				target_members += role.members

			if len(target_members):
				log_thread = await send_bulk_dm(interaction, target_members, log_thread, msg)

				notifyMe = f'\n__Content__\n'
				await log_thread.send(notifyMe)
				await log_thread.send(msg.strip())
			await log_thread.edit(archived=True)

		except Exception as ex:
			print('----- /tc_msg_member() -----')
			print(ex)
			await log_exception(ex, '/tc_msg_member', interaction)

	######################## DELETE A MSG ########################
	@message.sub_command(name = "remove")
	async def tc_remove_msg(interaction, msg_ids, channel_id):
		"""
		Delete msg from public/private - ,
		Parameters
		----------
		msg_ids: Messages IDs separated by , or space
		channel_id: Channel where to fetch the messages
		"""
		try:
			msg_ids = split_str(msg_ids)
			_ch = await bot.fetch_channel(channel_id)
			for msg_id in msg_ids:
				try:
					msg = await _ch.fetch_message(msg_id)
					await msg.delete()
				except Exception as ex:
					print(msg_id)
					pass
		except Exception as ex:
			print('----- /tc_remove_msg_member() -----')
			print(ex)
			await log_exception(ex, '/tc_remove_msg_member', interaction)

	@message.sub_command(name = "reactions")
	async def tc_get_message_reactions(interaction, msg_id, role: discord.Role = None):
		"""
		Get users who reacted to a message
		Parameters
		----------
		msg_id: Message ID
		role: assigned to reacting users
		"""
		try:
			msg = await interaction.channel.fetch_message(msg_id)
			feedbackText = f'https://discord.com/channels/{guildId}/{msg.channel.id}/{msg_id}\n'
			for r in msg.reactions:
				if len(feedbackText) > 1800:
					await interaction.send(f'Results : \n{feedbackText}', ephemeral=True)
					feedbackText = ''
				feedbackText += f'\n{r.emoji} / '
				async for u in r.users():
					try:
						if role: await u.add_roles(role)
						feedbackText += f'{u.mention} '
					except Exception as ex:
						pass
			await interaction.send(f'Results : \n{feedbackText}', ephemeral=True)
			if role: await interaction.send(f'Role : {role.mention}', ephemeral=True)
		except Exception as ex:
			print('---------- /tc_get_message_reactions() --------')
			print(ex)
			await log_exception(ex, '/tc_get_message_reactions', interaction)
