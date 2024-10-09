
from imports.actions.channel import *
from imports.actions.common import *
from imports.data_server.config import *
from imports.data_server.channels_categories import *

def init_slash_commands_category(params):
    
	bot = params['bot']
	discord = params['discord']
	
	@bot.slash_command(name="category")
	async def category(inter):
		pass
	
	@category.sub_command(name = "create")
	async def create_category(interaction, category_name:str, channel_name: str, channel_type: discord.ChannelType, count_category: int = 1, count_channel: int = 1):
		"""
		Create a multiple categories with multiple channels
		Parameters
		----------
		category : the category to create
		category_name : the name of the category to create
		channel_name : the name of the channel to create
		channel_type : the type of channel to create ("text", "voice", "forum", "stage")
		count_category : the number of categories to create (default 1)
		count_channel : the number of channels to create (default 1)
		"""
		try:
			if count_category < 1 or count_channel < 1:
				await interaction.send("Number of categories/channels to create should be > 0 !", ephemeral=True)
				return
			
			if channel_type not in [0, 2, 13, 15]:
				await interaction.send("No proper type was specified !", ephemeral=True)
				return
            
			if channel_type == 0:
				channel_type = "create_text_channel"
			if channel_type == 2:
				channel_type = "create_voice_channel"
			if channel_type == 15:
				channel_type = "create_forum_channel"
			if channel_type == 13:
				channel_type = "create_stage_channel"
			
			defaultRole = interaction.guild.get_role(roles['everyone'])
			for j in range(0, count_category):
				category = await interaction.guild.create_category(f"{category_name} #{j + 1}")
				await category.set_permissions(defaultRole, view_channel=False, send_messages=True,
											create_public_threads=True, create_private_threads=True,
											send_messages_in_threads=True, connect=True, speak=True, use_voice_activation=True)
                
				for i in range(0, count_channel):
					create_type_channel = getattr(category, channel_type)
					await create_type_channel(f"{channel_name} #{i + 1}")

			await interaction.send(f"{count_category} cat x {count_channel} ch = {count_category * count_channel} channels were created successfully !", ephemeral=True)
		except Exception as ex:
			print('----- /create_category() -----')
			print(ex)
			await log_exception(ex, '/create_category', interaction)
