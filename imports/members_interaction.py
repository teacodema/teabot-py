from setup.properties import *
from setup.actions import *

def init_members_interaction(params):

	client = params['client']
	slash = params['slash']
	discord = params['discord']

	######################## SEND MSG TO CHANNEL ########################
	@slash.slash(name = "msg_channel", guild_ids=[guildId])
	async def msg_channel(ctx, message, channel: discord.TextChannel):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return

			await channel.send(message)
			await ctx.send('Msg sent', delete_after = 2)
		
		except Exception as ex:
			print('----- /msg_channel -----')
			print(ex)

	######################## SEND MSG TO MEMBER ########################
	@slash.slash(name = "dm", guild_ids=[guildId])
	async def dm(ctx, message, member: discord.Member = None, role: discord.Role = None):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return

			await ctx.send("Sending direct message...", delete_after = 2)

			notifyMe = 'DM/'
			if role == None:
				if member == None: 
					member = ctx.author
				await send_msg(ctx, message, member)
				notifyMe += f'\n{message} --> Member: **{member.name}#{member.discriminator}**'
			else:
				if member != None:
					await send_msg(ctx, message, member)
					notifyMe += f'\n{message} --> Member: **{member.name}#{member.discriminator}**'
				members = role.members
				for member in members:
					await send_msg(ctx, message, member)
				notifyMe += f'\n{message} --> Role: **{role.name}**'
			
			channel = client.get_channel(textChannels['log-channel'])
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

