from setup.properties import *
from setup.actions import *

def init_role_activity(params):
	
	bot = params['bot']
	discord = params['discord']
	slash = params['slash']
	

	######################## ROLE ADD ########################
	@slash.slash(name="ar", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def assign(ctx, role: discord.Role, member: discord.Member = None, role2: discord.Role = None):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return

			await ctx.send('Assigning Role...', hidden=True)
			if (role2 != None and member == None):
				msg = f'{role2.mention} got a new role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(ctx, memberTo, role, True)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(ctx, member, role, True)
				msg = f'{member.mention} got a new role : {role.mention}'

			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /assign -----')
			print(ex)

	######################## ROLE TO MEMBERS ########################
	@slash.slash(name="arm", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def assign_to_members(ctx, role: discord.Role, members, assign: int = 1):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			
			await ctx.send('Updating Role...', hidden=True)
			guild = bot.get_guild(guildId)
			members = members.split('\\t')
			for m in members:
				try:
					m = m.replace('<@!', '')
					m = m.replace('>', '')
					m = await guild.fetch_member(m)
					await toggleRole(ctx, m, role, assign)
				except Exception as ex:
					print(ex)
					pass
		except Exception as ex:
			print('----- /assign_to_members -----')
			print(ex)


	######################## ROLE REMOVE ########################
	@slash.slash(name = "ur", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def unassign(ctx, role: discord.Role, member: discord.Member = None, role2: discord.Role = None):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			
			await ctx.send('Unassigning Role...', hidden=True)
			if (role2 != None and member == None):
				msg = f'{role2.mention} lost a role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(ctx, memberTo, role, False)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(ctx, member, role, False)
				msg = f'{member.mention} lost a role : {role.mention}'
			
			channel = bot.get_channel(textChannels['log-channel'])
			await channel.send(msg)
		except Exception as ex:
			print('----- /unassign -----')
			print(ex)



	######################## TOGGLE ROLE ########################
	async def toggleRole(ctx, member, role, assign = True):
		try:
			if assign:
				await member.add_roles(role)
			else:
				await member.remove_roles(role)
		except Exception as ex:
			print('----- toggleRole -----')
			print(ex)