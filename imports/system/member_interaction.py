from setup.properties import *
from setup.actions import *

def init_member_interaction(params):

	bot = params['bot']
	slash = params['slash']
	discord = params['discord']


	######################## REPLY TO MSG ########################
	@slash.slash(name = "emc", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def edit_msg_channel(ctx, content, msg_id, channel: discord.TextChannel, pin: int=0):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			msg = await channel.fetch_message(int(msg_id))
			content = content.replace("\\n", "\n")
			content = content.replace("\\t", "	")
			await msg.edit(content=content)
			if pin:
				await msg.pin()
			await ctx.send('Edit done', hidden=True)
		except Exception as ex:
			print('----- /edit_msg_channel() -----')
			print(ex)


	######################## REPLY TO MSG ########################
	@slash.slash(name = "rc", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def reply_channel(ctx, reply, msg_id, channel: discord.TextChannel):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			msg = await channel.fetch_message(int(msg_id))
			reply = reply.replace("\\n", "\n")
			reply = reply.replace("\\t", "	")
			await msg.reply(reply)
			await ctx.send('Reply sent', hidden=True)
		except Exception as ex:
			print('----- /reply_channel() -----')
			print(ex)


	######################## SEND MSG TO CHANNEL ########################
	@slash.slash(name = "mc", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def msg_channel(ctx, msg, channel: discord.TextChannel, pin: int=0):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			
			msg = msg.replace("\\n", "\n")
			msg = msg.replace("\\t", "	")
			msg = await channel.send(msg)
			if pin:
				await msg.pin()
			await ctx.send('Msg sent', hidden=True)
		
		except Exception as ex:
			print('----- /msg_channel() -----')
			print(ex)

	######################## SEND MSG TO MEMBER ########################
	@slash.slash(name = "mm", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def msg_member(ctx, msg, member: discord.Member = None, role: discord.Role = None):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return

			msg = msg.replace("\\n", "\n")
			msg = msg.replace("\\t", "	")
			await ctx.send("Sending direct message...", hidden=True)

			notifyMe = f'DM/ =▷'
			notifyMe+= f'\n__To__'
			if role == None:
				if member == None: 
					member = ctx.author
				_sentMsg = await send_msg(ctx, msg, member)
				notifyMe += f'\nmessage ID : {_sentMsg.id}'
				notifyMe += f'\nchannel ID : {_sentMsg.channel.id}'
				notifyMe += f'\nMember: **{member.mention}**'
			else:
				if member != None:
					_sentMsg = await send_msg(ctx, msg, member)
					notifyMe += f'\nmessage ID : {_sentMsg.id}'
					notifyMe += f'\nchannel ID : {_sentMsg.channel.id}'
					notifyMe += f'\nMember: **{member.mention}**'
				members = role.members
				for member in members:
					try:
						_sentMsg = await send_msg(ctx, msg, member)
						notifyMe += f'\nmessage ID : {_sentMsg.id}'
						notifyMe += f'\nchannel ID : {_sentMsg.channel.id}'
					except Exception as ex:
						print('----- /msg_member()/send_msg/role -----')
						print(ex)
						pass

				notifyMe += f'\nRole: **{role.mention}**'
			notifyMe += f'\n__Content__\n{msg}'
			
			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(notifyMe)

		except Exception as ex:
			print('----- /msg_member() -----')
			print(ex)

	######################## DELETE A MSG ########################
	@slash.slash(name = "rm", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def remove_msg_member(ctx, msg_ids, channel_id):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			await ctx.send("Deleting direct message...", hidden=True)
			msg_ids = msg_ids.split(',')
			_ch = await bot.fetch_channel(channel_id)
			for msg_id in msg_ids:
				msg = await _ch.fetch_message(msg_id)
				await msg.delete()
		except Exception as ex:
			print('----- /remove_msg_member() -----')
			print(ex)



	async def send_msg(ctx, message, member):
		try:
			channel = member.dm_channel
			if channel == None:
				channel = await member.create_dm()
			return await channel.send(message)
		except Exception as ex:
			print('----- send_msg() -----')
			print(ex)
			raise ex

