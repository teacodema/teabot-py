from setup.properties import *
from setup.actions import *

def init_role_activity(params):
	
	
	client = params['client']
	discord = params['discord']
	slash = params['slash']

	######################## ROLE ASSIGNE ########################
	@slash.slash(name="assign", description="Assign a role to a member", guild_ids=[guildId])
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
					await toggleRole(client, ctx, memberTo, role, True)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(client, ctx, member, role, True)
				msg = f'{member.mention} got a new role : {role.mention}'

			channel = client.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /assign -----')
			print(ex)


	@slash.slash(name = "unassign", description="Remove a role from a member", guild_ids = [guildId])
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
					await toggleRole(client, ctx, memberTo, role, False)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(client, ctx, member, role, False)
				msg = f'{member.mention} lost a role : {role.mention}'
			
			channel = client.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /unassign -----')
			print(ex)



######################## TOGGLE ROLE ########################
async def toggleRole(client, ctx, member, role, assign = True):
	try:
		if (assign):
			await member.add_roles(role)
		else:
			await member.remove_roles(role)
	except Exception as ex:
		print('----- toggleRole -----')
		print(ex)