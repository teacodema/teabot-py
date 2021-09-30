from setup.properties import *
from setup.actions import *
import time

def init_server_data(params):

	client = params['client']
	discord = params['discord']
	slash = params['slash']
	get = params['get']

	######################## ROLE ASSIGNE ########################
	@slash.slash(name="server-info", description = "Get server info/stats", guild_ids=[guildId])
	async def server_info(ctx):
		try:

			excludedCategories = [
				categories['staff-corner'],
				categories['moderators-corner'],
				categories['private-corner'],
				categories['lab-corner'],
				categories['system-corner'],
			]
			isNotAllowed = not is_founders(ctx)

			guild = client.get_guild(ctx.guild_id)

			_created_at = guild.created_at
			created_at = ''
			created_at += f'{_created_at.date().strftime("%A")}'
			created_at += f', {_created_at.date().strftime("%B")} {_created_at.day}'
			created_at += f', {_created_at.year}'
			created_at += f', {_created_at.hour}'
			created_at += f':{_created_at.minute}'

			embed = discord.Embed(title=guild.name, description="", color=0x1da1f2)

			embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)

			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Guild Name", value=guild.name, inline=True)
			embed.add_field(name="Created", value=created_at, inline=True)
			embed.add_field(name="Roles", value=len(guild.roles), inline=True)
			embed.add_field(name="Members", value=len(guild.members), inline=True)
			# embed.add_field(name="Channels", value=len(guild.channels), inline=True)
			
			if (isNotAllowed):
				total_categories = len(guild.categories) - len(excludedCategories)
			else:
				total_categories = len(guild.categories)
			
			embed.add_field(name="Categories", value=total_categories, inline=True)
			# embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
			# embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
			# embed.add_field(name="Stage Channels", value=len(guild.stage_channels), inline=True)

			total_text_channels = len(guild.text_channels)
			total_voice_channels = len(guild.voice_channels)
			total_stage_channels = len(guild.stage_channels)

			if (isNotAllowed):
				total_channels = 0
				for catId in excludedCategories:
					category = get(guild.categories, id = catId)
					total_text_channels -= len(category.text_channels)
					total_voice_channels -= len(category.voice_channels)
					total_stage_channels -= len(category.stage_channels)
					total_channels = total_text_channels + total_voice_channels + total_stage_channels
			else:
				total_channels = total_text_channels + total_voice_channels + total_stage_channels

			value = f'Total : {total_channels}'
			value += f'\nText : {total_text_channels}'
			value += f'\nVoice : {total_voice_channels}'
			value += f'\nStage : {total_stage_channels}'

			embed.add_field(name="Channels", value=value, inline=True)

			# embed.add_field(name="large", value=guild.large, inline=True)
			# embed.add_field(name="max mem", value=guild.max_members, inline=True)
			# embed.add_field(name="me", value=guild.me, inline=True)
			embed.set_footer(text=f"ID : {guild.id}")
			await ctx.send(embed=embed)

		except Exception as ex:
			print('----- /server-info -----')
			print(ex)

	######################## ROLE ASSIGNE ########################
	@slash.slash(name="role-info", description = "Get role info/stats", guild_ids=[guildId])
	async def role_info(ctx, role: discord.Role = None):
		try:

			if role == None:
				role = ctx.author.top_role
			else:
				roleIds = [role.id for role in ctx.author.roles]
				if not is_founders(ctx) and (role.id not in roleIds):
					await ctx.send('❌ You can only see data of roles you have')
					return

			embed = discord.Embed(name=f'Role : {ctx.author.display_name}', title=role.name, description="", color=role.color)
			
			# embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name="Name", value=role.name, inline=True)
			embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
			embed.add_field(name="Members", value=len(role.members), inline=True)
			embed.set_footer(text=f"ID : {role.id}")

			await ctx.send(embed=embed)

		except Exception as ex:
			print('----- /role-info -----')
			print(ex)

	######################## ROLE ASSIGNE ########################
	@slash.slash(name="member-info", description = "Get member info/stats", guild_ids=[guildId])
	async def member_info(ctx, member: discord.Member = None):
		try:

			roleIds = [role.id for role in ctx.author.roles]
			authorizedRoles = [roles['founders']]
			roleExists = [value for value in authorizedRoles if value in roleIds]

			if member == None:
				member = ctx.author
			else:
				if not is_founders(ctx):
					await ctx.send('❌ You can only see your data')
					member = ctx.author
					time.sleep(3)


			_created_at = member.created_at
			created_at = ''
			created_at += f'{_created_at.date().strftime("%A")}'
			created_at += f', {_created_at.date().strftime("%B")} {_created_at.day}'
			created_at += f', {_created_at.year}'
			created_at += f', {_created_at.hour}'
			created_at += f':{_created_at.minute}'

			_joined_at = member.joined_at
			joined_at = ''
			joined_at += f'{_joined_at.date().strftime("%A")}'
			joined_at += f', {_joined_at.date().strftime("%B")} {_joined_at.day}'
			joined_at += f', {_joined_at.year}'
			joined_at += f', {_joined_at.hour}'
			joined_at += f':{_joined_at.minute}'

			embed = discord.Embed(title=member.display_name, description="", color=member.top_role.color)

			embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)

			embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name="User Name", value=member.name, inline=True)
			embed.add_field(name="Nick Name", value=member.nick, inline=True)
			embed.add_field(name="Display Name", value=member.display_name, inline=True)
			embed.add_field(name="Joined", value=joined_at, inline=True)
			embed.add_field(name="Registred", value=created_at, inline=True)
			embed.add_field(name="Top Role", value=f'{member.top_role.mention}', inline=True)
			embed.add_field(name="Roles", value=len(member.roles) - 1, inline=True)
			embed.set_footer(text=f"ID : {member.id}")

			await ctx.send(embed=embed)

		except Exception as ex:
			print('----- /member-info -----')
			print(ex)

