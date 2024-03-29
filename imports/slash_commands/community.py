from imports.actions.common import *

def init_slash_commands_community(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']
	
	@bot.slash_command(name="community")
	async def community(inter):
		pass

	types = ["Topic for technical session", "Topic for a hangout", "Topic for the english session", "New activity"]
	@community.sub_command(name="suggest")
	async def suggest(interaction, content, type=commands.Param(choices=types)):
		"""
		Send a suggestion to the community staff
		Parameters
		----------
		content: Your suggestion text
		type: Choose a category from the list
		"""
		try:
			if type not in types: 
				await interaction.send(f'⚠ Issue with the input (choose one of the provided options)', ephemeral=True)

			channel = bot.get_channel(textChannels['log-community'])
			msg = "======== Suggestions ========"
			msg += f'\n{interaction.author.mention} sent a suggestion:'
			msg += f'\nType: {type}'
			msg += f'\nContent: {content}'
			msg += "\n==============================="
			await channel.send(msg.strip())
			
		except Exception as ex:
			print('----- /suggest() -----')
			print(ex)
			await log_exception(ex, '/suggest', interaction)
			

	@community.sub_command(name="interview")
	async def interview(interaction, resume: discord.Attachment, email):
		"""
		Send your resume to apply for a mock interview
		Parameters
		----------
		resume: PDF file <= 1MB with a short name
		email: Get the answer via your email
		"""
		try:
			if (resume.content_type != 'application/pdf' 
				or not resume.filename.endswith('.pdf')):
				await interaction.send('Resume should be a pdf file !!!', ephemeral=True)
				return
			if resume.size > 1_000_000:
				await interaction.send('Resume file size should be less than 1 MB !!!', ephemeral=True)
				return
			if len(resume.filename) > 100:
				await interaction.send('Resume file name is too long !!!', ephemeral=True)
				return

			channel = bot.get_channel(textChannels['log-community'])
			resume_file = await resume.to_file()
			msg = "======== Mock Interview ========"
			msg += f'\n{interaction.author.mention} requested a mock interview:'
			msg += f'\nResume file : {resume.url}'
			msg += f'\nEmail : {email}'
			msg += "\n==============================="
			await channel.send(content=msg.strip(), file=resume_file)
			feedback = "You will get a response in a few days.\nThank you"
			await interaction.send(feedback.strip(), ephemeral=True)
		except Exception as ex:
			print('----- /interview() -----')
			print(ex)
			await log_exception(ex, '/interview', interaction)