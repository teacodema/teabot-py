from imports.data_common.config import *
from imports.actions.common import *

def init_slash_commands_info(params):

	bot = params['bot']
	discord = params['discord']

	@bot.slash_command(name="server")
	async def server(inter):
		pass

	######################## SERVER INFO ########################
	@server.sub_command(name = "info")
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

