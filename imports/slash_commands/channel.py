
from imports.actions.channel import *
from imports.actions.common import *
from imports.data_server.config import *
from imports.data_server.channels_categories import *

def init_slash_commands_channel(params):
	
	bot = params['bot']
	discord = params['discord']
	
	@bot.slash_command(name="channel")
	async def channel(inter):
		pass

	@channel.sub_command(name = "hide")
	async def tc_hide_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unhide:int = 0):
		"""
		Hide/Unhide channel for a role
		Parameters
		----------
		channel: target channel/category
		role: role to be affected by the change
		unhide: display the channel/category for the role - values 0/1 - default 0
		"""
		try:
			await toggle_hide_channel(channel, role, bool(unhide))
		except Exception as ex:
			print('----- /tc_hide_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_hide_channel', interaction)

	@channel.sub_command(name = "lock")
	async def tc_lock_channel(interaction, channel: discord.abc.GuildChannel, role: discord.Role, unlock:int = 0):
		"""
		Lock/Unlock channel for a role
		Parameters
		----------
		channel: target channel
		role: role to be affected by the change
		unlock: unlock the channel/category for the role - values 0/1 - default 0
		"""
		try:
			await toggle_lock_channel(channel, role, bool(unlock))
		except Exception as ex:
			print('----- /tc_lock_channel() -----')
			print(ex)
			await log_exception(ex, '/tc_lock_channel', interaction)

	@channel.sub_command(name = "voice-clone")
	async def clone_voice_channel(interaction, channel:discord.VoiceChannel, name = None):
		"""
		Clone a voice channel
		Parameters
		----------
		channel: Voice channel to clone
		name: Channel name (optional)
		"""
		try:
			excludedCategories = [
				categories['voice-channels'],
				categories['help-voice'],
			]
			if channel.category_id not in excludedCategories:
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Cloning...', ephemeral=True)
			if (name == None) or (name == channel.name):
				name = f'{channel.name} / (cloned)'
			await channel.clone(name = name)
		except Exception as ex:
			print('----- /clone_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/clone_voice_channel', interaction)

	@channel.sub_command(name = "voice-delete")
	async def delete_voice_channel(interaction, channel:discord.VoiceChannel):
		"""
		Delete a voice channel
		Parameters
		----------
		channel: Voice channel to delete
		"""
		try:
			excludedCategories = [
				categories['voice-channels'],
				categories['help-voice'],
			]
			if (channel.category_id not in excludedCategories) or (channel.id in protected_voiceChannels):
				await interaction.send('❌ Channel not allowed', ephemeral=True)
				return
			await interaction.send(f'Deleting...', ephemeral=True)
			await channel.delete()
		except Exception as ex:
			print('----- /delete_voice_channel() -----')
			print(ex)
			await log_exception(ex, '/delete_voice_channel', interaction)

	@channel.sub_command(name = "channel-info")
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
			embed.add_field(name="Channel Name", value=channel.name, inline=True)
			embed.add_field(name="Channel Type", value=channel.type, inline=True)
			if hasattr(channel, 'category') and channel.category:
				print(channel.category)
				embed.add_field(name="Category", value=channel.category.name, inline=True)
			embed.add_field(name="Created", value=created_at, inline=True)
			if hasattr(channel, 'members'): 
				embed.add_field(name="Members", value=len(channel.members), inline=True)
			if hasattr(channel, 'threads'): 
				embed.add_field(name="Threads", value=len(channel.threads), inline=True)

			# embed.set_footer(text=f"ID : {member.id}")
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /channel-info() -----')
			print(ex)
			await log_exception(ex, '/channel-info', interaction)
