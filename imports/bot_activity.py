from setup.properties import *
from setup.actions import *

def init_bot_activity(params):

	client = params['client']
	discord = params['discord']
	slash = params['slash']

	states = ["online", "dnd", "idle", "offline"]
	discord_states = [
		discord.Status.online, discord.Status.dnd, discord.Status.idle
	]
	types = ["watching", "listening", "playing"]
	discord_types = [
		discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing
	]
	
	######################## BOT READY ########################
	@client.event
	async def on_ready():
		try:
			await startBot(client, discord)
		except Exception as ex:
			print('----- on_ready -----')
			print(ex)

	######################## BOT STATE ########################
	@slash.slash(name = "state", description = "Change current state. (online, dnd, idle)", guild_ids = [guildId])
	async def change_state(ctx, state = "online"):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			await client.change_presence(status = discord_states[states.index(state)])
			await ctx.send("State has been changed")
		except Exception as ex:
			# await client.change_presence(status = discord_states[0])
			# await ctx.send("Invalid state")
			print('----- /state -----')
			print(ex)

	######################## BOT ACTIVITY ########################
	@slash.slash(name = "activity", description = "Change current activity. type:(watching, playing, streaming, listening)", guild_ids = [guildId])
	async def change_activity(ctx, type, value):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
				
			activity = discord.Activity(type = discord_types[types.index(type)], name = value)
			await client.change_presence(activity = activity)
			await ctx.send("Activity changed")
		except Exception as ex:
			await client.change_presence(activity = None)
			await ctx.send("Invalid activity type")
			print('----- /activity -----')
			print(ex)


######################## BOT READY ########################
async def startBot(client, discord):
	try:
		print("We have logged in as {0.user}".format(client))
		status = discord.Status.online
		# activity = discord.Activity(type=discord.ActivityType.watching, name="teacode.ma")
		# activity = discord.Game(name="https://teacode.ma", type=3)
		activity = discord.Activity(type=discord.ActivityType.watching, name="🌐 teacode.ma ☕")
		# class discord.CustomActivity(name, *, emoji=None, **extra)
		await client.change_presence(status=status, activity=activity)
	except Exception as ex:
		print('----- startBot -----')
		print(ex)


