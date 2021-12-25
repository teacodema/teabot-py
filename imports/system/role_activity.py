from setup.properties import *
from setup.actions import *

def init_role_activity(params):
	
	bot = params['bot']
	get = params['get']
	discord = params['discord']
	slash = params['slash']
	

	######################## TOGGLE ADD ########################
	@slash.slash(name = "tr", guild_ids = [guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def toggle_role(ctx, role: discord.Role, member: discord.Member = None, role2: discord.Role = None, assign:int = 1):
		try:

			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return

			await ctx.send('Toggling Role...', hidden=True)
			if (role2 != None and member == None):
				msg = f'{role2.mention} {"got" if assign else "lost"} a role : {role.mention}'
				members = role2.members
				for memberTo in members:
					await toggleRole(ctx, memberTo, role, assign)
			else:
				if (not member):
					member = ctx.author
				await toggleRole(ctx, member, role, assign)
				msg = f'{member.mention} {"got" if assign else "lost"} a role : {role.mention}'

			await ctx.send(msg, hidden=True)
		except Exception as ex:
			print('----- /toggle_role() -----')
			print(ex)


	######################## ROLE TO MEMBERS ########################
	@slash.slash(name="trm", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def toggle_role_members(ctx, roles, members, assign: int = 1):
		try:
			
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions')
				return
			
			await ctx.send('Updating Role...', hidden=True)
			guild = bot.get_guild(guildId)

			msg_r = ''
			roles = roles.split(',')
			roles_list = []
			for role_id in roles:
				role_id = role_id.replace('<@&', '')
				role_id = role_id.replace('>', '')
				role = get(guild.roles, id = int(role_id))
				msg_r += f'{role.mention}, '
				roles_list.append(role)

			msg_m = ''
			members = members.split(',')
			for m in members:
				try:
					m = m.replace('<@!', '')
					m = m.replace('>', '')
					m = await guild.fetch_member(m)
					msg_m += f'{m.mention}, '
					await toggleRole(ctx, m, roles_list, assign)
				except Exception as ex:
					print('----- /toggle_role_members()/toggle member -----')
					print(ex)
					pass

			msg = f'{msg_m} {"got" if assign else "lost"} roles : {msg_r}'
			await ctx.send(msg, hidden=True)
		except Exception as ex:
			print('----- /toggle_role_members() -----')
			print(ex)


	######################## TOGGLE ROLE ########################
	async def toggleRole(ctx, member, roles, assign = True):
		try:
			if assign:
				await member.add_roles(*roles)
			else:
				await member.remove_roles(*roles)
		except Exception as ex:
			print('----- toggleRole() -----')
			print(ex)