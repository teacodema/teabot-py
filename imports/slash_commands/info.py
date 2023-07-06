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
			excludedCategories = [
				categories['committee-corner'],
				categories['log-corner'],
				categories['lab-corner'],
				categories['system-corner'],
			]
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
			
			if is_root(guild, interaction.author): total_categories = len(guild.categories)
			else: total_categories = len(guild.categories) - len(excludedCategories)
			
			embed.add_field(name="Categories", value=total_categories, inline=True)
			# embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
			# embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
			# embed.add_field(name="Stage Channels", value=len(guild.stage_channels), inline=True)

			total_text_channels = len(guild.text_channels)
			total_voice_channels = len(guild.voice_channels)
			total_stage_channels = len(guild.stage_channels)

			if is_root(guild, interaction.author): total_channels = total_text_channels + total_voice_channels + total_stage_channels
			else:
				total_channels = 0
				for catId in excludedCategories:
					category = guild.get_channel(catId)
					total_text_channels -= len(category.text_channels)
					total_voice_channels -= len(category.voice_channels)
					total_stage_channels -= len(category.stage_channels)
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
			if is_root(guild, interaction.author): embed.add_field(name="Server ID", value=guild.id, inline=True)
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
			embed = discord.Embed(title=role.name, description="", color=role.color)
			# embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name="Name", value=role.name, inline=True)
			embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
			embed.add_field(name="Members", value=len(role.members), inline=True)
			embed.add_field(name="Position", value=role.position, inline=True)
			embed.add_field(name="Mention", value=role.mention, inline=True)
			embed.add_field(name="Color", value=role.color, inline=True)
			if is_root(interaction.guild, interaction.author): embed.add_field(name="Role ID", value=role.id, inline=True)
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
			created_at = getTimeUtcPlusOne(member.created_at, "%A, %B %d, %Y - %H:%M")
			joined_at = getTimeUtcPlusOne(member.joined_at, "%A, %B %d, %Y - %H:%M")

			embed = discord.Embed(title=member.display_name, description="", color=member.color)
			embed.set_author(name=f'{member.name}', icon_url=member.display_avatar)
			embed.set_thumbnail(url=member.display_avatar)
			embed.add_field(name="User Name", value=member.name, inline=True)
			embed.add_field(name="Nick Name", value=member.nick, inline=True)
			embed.add_field(name="Display Name", value=member.display_name, inline=True)
			embed.add_field(name="Registred", value=created_at, inline=True)
			embed.add_field(name="Joined", value=joined_at, inline=True)
			embed.add_field(name="Top Role", value=f'{member.top_role.mention}', inline=True)
			embed.add_field(name="Roles", value=len(member.roles) - 1, inline=True)
			embed.add_field(name="Mention", value=member.mention, inline=True)
			embed.add_field(name="Color", value=member.color, inline=True)
			if is_root(interaction.guild, interaction.author): embed.add_field(name="Member ID", value=member.id, inline=True)
			# embed.set_footer(text=f"ID : {member.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /member-info() -----')
			print(ex)
			await log_exception(ex, '/member-info', interaction)

	######################## CHANNEL INFO ########################
	@info.sub_command(name = "channel")
	async def channel_info(interaction, channel: discord.abc.GuildChannel):
		"""
		Get channel info/stats
		Parameters
		----------
		channel: Server existing channel
		"""
		try:
			created_at = getTimeUtcPlusOne(channel.created_at, "%A, %B %d, %Y - %H:%M")
			member = interaction.author
			embed = discord.Embed(title=channel.name, description="", color=member.color)
			embed.set_author(name=f'{channel.name}', icon_url=interaction.guild.icon.url)
			embed.set_thumbnail(url=interaction.guild.icon.url)
			embed.add_field(name="Name", value=channel.name, inline=True)
			embed.add_field(name="Type", value=channel.type, inline=True)
			if hasattr(channel, 'category') and channel.category:
				embed.add_field(name="Category", value=channel.category.name, inline=True)
			embed.add_field(name="Created", value=created_at, inline=True)
			if hasattr(channel, 'members'): 
				embed.add_field(name="Members", value=len(channel.members), inline=True)
			if hasattr(channel, 'threads') and channel.threads:
				embed.add_field(name="Threads", value=len(channel.threads), inline=True)
			
			if hasattr(channel, 'topic') and channel.topic:
				embed.add_field(name="Topic", value=channel.topic, inline=True)
			if hasattr(channel, 'threads') and channel.threads:
				embed.add_field(name="Threads", value=len(channel.threads), inline=True)
			if hasattr(channel, 'moderators') and channel.moderators:
				embed.add_field(name="Moderators", value=len(channel.moderators), inline=True)
				
			if not hasattr(channel, 'category'):
				embed.add_field(name="Channels", value=len(channel.channels), inline=True)
				embed.add_field(name="Forum Channels", value=len(channel.forum_channels), inline=True)
		
			if hasattr(channel, 'position') and channel.position:
				embed.add_field(name="Position", value=channel.position, inline=True)
			embed.add_field(name="Url", value=channel.jump_url, inline=True)
			embed.add_field(name="Mention", value=channel.mention, inline=True)

			if is_root(interaction.guild, interaction.author): embed.add_field(name="Channel ID", value=channel.id, inline=True)
			# embed.set_footer(text=f"ID : {member.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /channel-info() -----')
			print(ex)
			await log_exception(ex, '/channel-info', interaction)
