import json, os

def init_slash_commands_temporary(params):
	
	bot = params['bot']
	discord = params['discord']
    
	@bot.slash_command(name="roles-file")
	async def roles_file(interaction):
		json_filtered_members = []
		for role in interaction.guild.roles:
			object = {"role_name":role.id, "name":role.name, "position":role.position}
			json_filtered_members.append(object)
		json_filtered_members = sorted(json_filtered_members, key=lambda obj: obj['position'])
		json_data = json.dumps(json_filtered_members)
		with open("file.json", "w") as outfile:
			outfile.write(json_data)
		file = discord.File("file.json")
		await interaction.send(file=file, ephemeral=True)
		os.remove("file.json")
