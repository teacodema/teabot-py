from imports.data_common.config import *
from imports.actions.common import *

def init_slash_commands_info(params):

	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name="info")
	async def info(inter):
		pass

	######################## SERVER INFO ########################
	@info.sub_command(name = "server")
	async def server_info(interaction):
		"""
		Display server info
		"""
		try:
			# excludedCategories = [
			# 	categories['staff-corner'],
			# 	categories['private-corner'],
			# 	categories['lab-corner'],
			# 	categories['system-corner'],
			# ]
			# isNotAllowed = not is_founders(interaction)
			guild = interaction.guild
			created_at = getTimeUtcPlusOne(guild.created_at, "%A, %B %d, %Y - %H:%M")

			embed = discord.Embed(title=guild.name, description="", color=appParams['blue'])
			embed.set_author(name=f'{guild.name}', icon_url=guild.icon.url)
			embed.set_thumbnail(url=guild.icon.url)
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
			await interaction.send(embed=embed, ephemeral=True)

		except Exception as ex:
			print('----- /server-info() -----')
			print(ex)
			await log_exception(ex, '/server-info', interaction)


	######################## ROLE INFO ########################
	@info.sub_command(name = "role")
	async def role_info(interaction, role: discord.Role):
		"""
		Get role info/stats
		Parameters
		----------
		role: Server existing role
		"""
		try:
			# else:
			# 	guild = interaction.guild
			# 	_role = guild.get_role(roles['helpers']) # Helpers
			# 	action_name = inspect.stack()[0][3]
			# 	if not is_allowed(interaction, action_name) and role not in interaction.author.roles and role.position > _role.position:
			# 		await interaction.send('❌ You cannot see this data')
			# 		return

			embed = discord.Embed(title=role.name, description="", color=role.color)
			# embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name="Name", value=role.name, inline=True)
			embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
			embed.add_field(name="Members", value=len(role.members), inline=True)
			embed.add_field(name="Position", value=role.position, inline=True)
			embed.add_field(name="Mention", value=role.mention, inline=True)
			embed.add_field(name="Color", value=role.color, inline=True)
			# embed.set_footer(text=f"ID : {role.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")

			await interaction.send(embed=embed, ephemeral=True)

		except Exception as ex:
			print('----- /role-info() -----')
			print(ex)
			await log_exception(ex, '/role-info', interaction)

	######################## MEMBER INFO ########################
	@info.sub_command(name = "member")
	async def member_info(interaction, member: discord.Member):
		"""
		Get member info/stats
		Parameters
		----------
		member: Server existing member
		"""
		try:
			# else:
			# 	action_name = inspect.stack()[0][3]
			# 	if not is_allowed(interaction, action_name):
			# 		await interaction.send('❌ You can only see your data')
			# 		member = interaction.author

			created_at = getTimeUtcPlusOne(member.created_at, "%A, %B %d, %Y - %H:%M")
			joined_at = getTimeUtcPlusOne(member.joined_at, "%A, %B %d, %Y - %H:%M")

			embed = discord.Embed(title=member.display_name, description="", color=member.color)
			embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.display_avatar)
			embed.set_thumbnail(url=member.display_avatar)
			embed.add_field(name="User Name", value=member.name, inline=True)
			embed.add_field(name="Nick Name", value=member.nick, inline=True)
			embed.add_field(name="Display Name", value=member.display_name, inline=True)
			embed.add_field(name="Joined", value=joined_at, inline=True)
			embed.add_field(name="Registred", value=created_at, inline=True)
			embed.add_field(name="Top Role", value=f'{member.top_role.mention}', inline=True)
			embed.add_field(name="Roles", value=len(member.roles) - 1, inline=True)
			embed.add_field(name="Mention", value=member.mention, inline=True)
			embed.add_field(name="Color", value=member.color, inline=True)
			# embed.set_footer(text=f"ID : {member.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /member-info() -----')
			print(ex)
			await log_exception(ex, '/member-info', interaction)
