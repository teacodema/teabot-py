import datetime
import pytz
from setup.properties import *
from setup.actions import *

def init_bot_activity(params):

	bot = params['bot']
	# client2 = params['client2']
	discord = params['discord']
	# slash = params['slash']
	get = params['get']
	tasks = params['tasks']

	# states = ["online", "dnd", "idle", "offline"]
	# discord_states = [
	# 	discord.Status.online, discord.Status.dnd, discord.Status.idle
	# ]
	# types = ["watching", "listening", "playing"]
	# discord_types = [
	# 	discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing
	# ]

	######################## BOT READY ########################
	@bot.event
	async def on_ready():
		try:
			await startBot(bot, discord)
			start_loop()
		except Exception as ex:
			print('----- on_ready -----')
			print(ex)
		

	######################## BOT STATE ########################
	# @slash.slash(name = "state", description = "Change current state. (online, dnd, idle)", guild_ids = [guildId])
	# async def change_state(ctx, state = "online"):
	# 	try:

	# 		if not is_founders(ctx):
	# 			await ctx.send('❌ Missing Permissions', delete_after = 2)
	# 			return
			
	# 		await client.change_presence(status = discord_states[states.index(state)])
	# 		await ctx.send("State has been changed")
	# 	except Exception as ex:
	# 		# await client.change_presence(status = discord_states[0])
	# 		# await ctx.send("Invalid state")
	# 		print('----- /state -----')
	# 		print(ex)

	######################## BOT ACTIVITY ########################
	# @slash.slash(name = "activity", description = "Change current activity. type:(watching, playing, streaming, listening)", guild_ids = [guildId])
	# async def change_activity(ctx, type, value):
	# 	try:
			
	# 		if not is_founders(ctx):
	# 			await ctx.send('❌ Missing Permissions', delete_after = 2)
	# 			return
				
	# 		activity = discord.Activity(type = discord_types[types.index(type)], name = value)
	# 		await client.change_presence(activity = activity)
	# 		await ctx.send("Activity changed")
	# 	except Exception as ex:
	# 		await client.change_presence(activity = None)
	# 		await ctx.send("Invalid activity type")
	# 		print('----- /activity -----')
	# 		print(ex)
	
	def start_loop():
		@tasks.loop(hours=48, count=None, reconnect=False)
		async def check_membership_loop():
			try:
				updatedMembers = await checkNewMemberRole(bot, get)
				logChannel = bot.get_channel(textChannels['log-channel'])
				msg = ''
				updatedMembersCount = len(updatedMembers)
				if updatedMembersCount:
					for member in updatedMembers:
						msg += f'{member} , '

				await logChannel.send(f'{updatedMembersCount} updated members.\n{msg}')
			except Exception as ex:
					print('----- /check_membership_loop -----')
					print(ex)
					
		check_membership_loop.start()
		
		@tasks.loop(hours=2, count=None, reconnect=False)
		async def am_alive():
			# user = client2.get_user(users['drissboumlik'])
			# user = client.get_user(users['drissboumlik'])
			# channel = user.dm_channel
			channel = bot.get_channel(textChannels['log-bot'])
			timeZ_Ma = pytz.timezone('Africa/Casablanca')
			dt_Ma = datetime.now(timeZ_Ma)
			await channel.send(f'<:teacode_bordred:844450911941165086> am alive - {dt_Ma.strftime("%d %B %Y - %H:%M")}')

		am_alive.start()


######################## BOT READY ########################
async def startBot(bot, discord):
	try:
		print("We have logged in as {0.user}".format(bot))
		status = discord.Status.online
		# activity = discord.Activity(type=discord.ActivityType.watching, name="teacode.ma")
		# activity = discord.Game(name="https://teacode.ma", type=3)
		activity = discord.Activity(type=discord.ActivityType.watching, name="🌐 teacode.ma ☕")
		# class discord.CustomActivity(name, *, emoji=None, **extra)
		await bot.change_presence(status=status, activity=activity)
	except Exception as ex:
		print('----- startBot -----')
		print(ex)


