from setup.properties import *
from setup.actions import *

def init_members_interaction(params):

	bot = params['bot']
	slash = params['slash']
	discord = params['discord']
	create_permission = params['create_permission']
	SlashCommandPermissionType = params['SlashCommandPermissionType']

	######################## SEND MSG TO CHANNEL ########################
	@slash.slash(name = "mc", guild_ids=[guildId],
		permissions={ guildId: [
				create_permission(roles['members'], SlashCommandPermissionType.ROLE, False),
				create_permission(roles['everyone'], SlashCommandPermissionType.ROLE, False),
				create_permission(roles['founders'], SlashCommandPermissionType.ROLE, True)
			]})
	async def msg_channel(ctx, msg, channel: discord.TextChannel):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			msg = msg.replace("\\n", "\n")
			msg = msg.replace("\\t", "	")
			await channel.send(msg)
			await ctx.send('Msg sent', delete_after = 2)
		
		except Exception as ex:
			print('----- /msg_channel -----')
			print(ex)

	######################## SEND MSG TO MEMBER ########################
	@slash.slash(name = "mm", guild_ids=[guildId],
		permissions={ guildId: [ 
				create_permission(roles['members'], SlashCommandPermissionType.ROLE, False),
				create_permission(roles['everyone'], SlashCommandPermissionType.ROLE, False),
				create_permission(roles['founders'], SlashCommandPermissionType.ROLE, True)
			]})
	async def msg_member(ctx, msg, member: discord.Member = None, role: discord.Role = None):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return

			msg = msg.replace("\\n", "\n")
			msg = msg.replace("\\t", "	")
			await ctx.send("Sending direct message...", delete_after = 2)

			notifyMe = 'DM/'
			if role == None:
				if member == None: 
					member = ctx.author
				await send_msg(ctx, msg, member)
				notifyMe += f'\n{msg} ➜ Member: **{member.mention}**'
			else:
				if member != None:
					await send_msg(ctx, msg, member)
					notifyMe += f'\n{msg} ➜ Member: **{member.mention}**'
				members = role.members
				for member in members:
					await send_msg(ctx, msg, member)
				notifyMe += f'\n{msg} ➜ Role: **{role.mention}**'
			
			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(notifyMe)

		except Exception as ex:
			print('----- /dm -----')
			print(ex)


async def send_msg(ctx, message, member):
	try:
		channel = member.dm_channel
		if channel == None:
			channel = await member.create_dm()
		await channel.send(message)
	except Exception as ex:
		print('----- send_msg -----')
		print(ex)

