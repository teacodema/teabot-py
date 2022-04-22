from setup.properties import *
from setup.actions import *

def init_server_data(params):

	bot = params['bot']
	discord = params['discord']
	slash = params['slash']
	get = params['get']

	######################## SERVER INFO ########################
	@slash.slash(name="si", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def server_info(ctx, hidden: int = 0):
		try:
			excludedCategories = [
				categories['moderators-corner'],
				categories['private-corner'],
				categories['lab-corner'],
				categories['system-corner'],
			]
			isNotAllowed = not is_founders(ctx)

			guild = bot.get_guild(ctx.guild_id)

			created_at = getTimeUtcPlusOne(guild.created_at, "%A, %B %d, %Y - %H:%M")

			embed = discord.Embed(title=guild.name, description="", color=0x1da1f2)
			embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.set_thumbnail(url=guild.icon_url)
			embed.add_field(name="Guild Name", value=guild.name, inline=True)
			embed.add_field(name="Created", value=created_at, inline=True)
			embed.add_field(name="Roles", value=len(guild.roles), inline=True)
			embed.add_field(name="Members", value=len(guild.members), inline=True)
			# embed.add_field(name="Channels", value=len(guild.channels), inline=True)
			
			# if (isNotAllowed):
			# 	total_categories = len(guild.categories) - len(excludedCategories)
			# else:
			total_categories = len(guild.categories)
			
			embed.add_field(name="Categories", value=total_categories, inline=True)
			# embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
			# embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
			# embed.add_field(name="Stage Channels", value=len(guild.stage_channels), inline=True)

			total_text_channels = len(guild.text_channels)
			total_voice_channels = len(guild.voice_channels)
			total_stage_channels = len(guild.stage_channels)

			# if (isNotAllowed):
			# 	total_channels = 0
			# 	for catId in excludedCategories:
			# 		category = get(guild.categories, id = catId)
			# 		total_text_channels -= len(category.text_channels)
			# 		total_voice_channels -= len(category.voice_channels)
			# 		total_stage_channels -= len(category.stage_channels)
			# 		total_channels = total_text_channels + total_voice_channels + total_stage_channels
			# else:
			total_channels = total_text_channels + total_voice_channels + total_stage_channels

			value = f'Total : {total_channels}'
			value += f'\nText : {total_text_channels}'
			value += f'\nVoice : {total_voice_channels}'
			value += f'\nStage : {total_stage_channels}'

			embed.add_field(name="Channels", value=value, inline=True)
			# embed.add_field(name="large", value=guild.large, inline=True)
			# embed.add_field(name="max mem", value=guild.max_members, inline=True)
			# embed.add_field(name="me", value=guild.me, inline=True)
			# embed.set_footer(text=f"ID : {guild.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await ctx.send(embed=embed, hidden=bool(hidden))

		except Exception as ex:
			print('----- /server-info() -----')
			print(ex)
			await log_exception(ex, '/server-info', ctx)

	######################## ROLE INFO ########################
	@slash.slash(name="role-info", description = "Get role info/stats", guild_ids=[guildId])
	async def role_info(ctx, role: discord.Role = None, hidden: int = 0):
		try:
			if role == None:
				role = ctx.author.top_role
			else:
				guild = bot.get_guild(guildId)
				_role = get(guild.roles, id = 799370946372698113) # 🍃│Helpers
				if not is_founders(ctx) and role not in ctx.author.roles and role.position > _role.position:
					await ctx.send('❌ You cannot see this data')
					return

			embed = discord.Embed(name=f'Role : {ctx.author.display_name}', title=role.name, description="", color=role.color)
			# embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name="Name", value=role.name, inline=True)
			embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
			embed.add_field(name="Members", value=len(role.members), inline=True)
			# embed.set_footer(text=f"ID : {role.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")

			await ctx.send(embed=embed, hidden=bool(hidden))

		except Exception as ex:
			print('----- /role-info() -----')
			print(ex)
			await log_exception(ex, '/role-info', ctx)

	######################## MEMBER INFO ########################
	@slash.slash(name="member-info", description = "Get member info/stats", guild_ids=[guildId])
	async def member_info(ctx, member: discord.Member = None, hidden : int = 0):
		try:

			if member == None or member == ctx.author:
				member = ctx.author
			else:
				if not is_founders(ctx):
					await ctx.send('❌ You can only see your data')
					member = ctx.author

			created_at = getTimeUtcPlusOne(member.created_at, "%A, %B %d, %Y - %H:%M")
			joined_at = getTimeUtcPlusOne(member.joined_at, "%A, %B %d, %Y - %H:%M")

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
			# embed.set_footer(text=f"ID : {member.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await ctx.send(embed=embed, hidden=bool(hidden))
		except Exception as ex:
			print('----- /member-info() -----')
			print(ex)
			await log_exception(ex, '/member-info', ctx)

