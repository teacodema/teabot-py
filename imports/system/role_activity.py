from setup.properties import *
from setup.actions import *

def init_role_activity(params):
	
	bot = params['bot']
	discord = params['discord']
	slash = params['slash']
	

	######################## ROLE ADD ########################
	# @bot.command(name="assign", pass_context=True)
	@slash.slash(name="assign", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def assign(ctx, role: discord.Role, member: discord.Member = None, role2: discord.Role = None):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return

			await ctx.send('Assigning Role', delete_after = 2)
			if (role2 != None and member == None):
				msg = f'{role2.mention} got a new role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(bot, ctx, memberTo, role, True)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(bot, ctx, member, role, True)
				msg = f'{member.mention} got a new role : {role.mention}'

			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /assign -----')
			print(ex)

	######################## ROLE REMOVE ########################
	# @bot.command(name="unassign", pass_context=True)
	@slash.slash(name = "unassign", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def unassign(ctx, role: discord.Role, member: discord.Member = None, role2: discord.Role = None):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', delete_after = 2)
				return
			
			await ctx.send('Unassigning Role', delete_after = 2)
			if (role2 != None and member == None):
				msg = f'{role2.mention} lost a role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(bot, ctx, memberTo, role, False)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(bot, ctx, member, role, False)
				msg = f'{member.mention} lost a role : {role.mention}'
			
			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /unassign -----')
			print(ex)



######################## TOGGLE ROLE ########################
async def toggleRole(bot, ctx, member, role, assign = True):
	try:
		if (assign):
			await member.add_roles(role)
		else:
			await member.remove_roles(role)
	except Exception as ex:
		print('----- toggleRole -----')
		print(ex)