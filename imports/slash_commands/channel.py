
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
		unhide: display the channel/category for the role - enter 1 to activate (default 0)
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
		unlock: unlock the channel/category for the role - enter 1 to activate (default 0)
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

	@channel.sub_command(name = "create")
	async def create_channel(interaction, category_name:str, channel_name: str, channel_type: discord.ChannelType, category: discord.CategoryChannel = None, count: int = 1):
		"""
		Create a new channel with the given category
		Parameters
		----------
		category : the category to create
		category_name : the name of the category to create
		channel_name : the name of the channel to create
		channel_type : the type of channel to create ("text", "voice", "forum", "stage")
		count : the number of channels to create (default 1)
		"""
		try:
			if count < 1:
				await interaction.send("Number of channels to create should be > 0 !", ephemeral=True)
				return
			if category == None :
				category = await interaction.guild.create_category(category_name)
				memberRole = interaction.guild.get_role(roles['everyone'])
				await category.set_permissions(memberRole, view_channel=False,
											send_messages=True,
											create_public_threads=True,
											create_private_threads=True,
											send_messages_in_threads=True,
											connect=True,
											speak=True,
											use_voice_activation=True
                                        )
			
			create_type_channel = None
			if channel_type == 0:
				create_type_channel = category.create_text_channel
			if channel_type ==  2:
				create_type_channel = category.create_voice_channel
			if channel_type == 15:
				create_type_channel = category.create_forum_channel
			if channel_type == 13:
				create_type_channel = category.create_stage_channel
			
			if create_type_channel == None:
				await interaction.send("No proper type was specified !", ephemeral=True)
				return

			await create_type_channel(channel_name)
			
			if count > 1:
				for i in range(1, count):
					await create_type_channel(f"{channel_name} #{i + 1}")
				
			await interaction.send(f"{count} channel(s) were created successfully !", ephemeral=True)
		except Exception as ex:
			print('----- /create_channel() -----')
			print(ex)
			await log_exception(ex, '/create_channel', interaction)

	@channel.sub_command(name = "delete")
	async def delete_channel(interaction, channel: discord.abc.GuildChannel):
		"""
		Create a new channel with the given category
		Parameters
		----------
		channel: channel/category to be deleted
		"""
		try:
			if channel.type == discord.ChannelType.category:
				for c in channel.forum_channels:
					await c.delete()
				for c in channel.stage_channels:
					await c.delete()
				for c in channel.text_channels:
					await c.delete()
				for c in channel.voice_channels:
					await c.delete()
			await channel.delete()
				
			await interaction.send(f"{channel} is deleted successfully !", ephemeral=True)
			
		except Exception as ex:
			print('----- /create_channel() -----')
			print(ex)
			await log_exception(ex, '/create_channel', interaction)
		