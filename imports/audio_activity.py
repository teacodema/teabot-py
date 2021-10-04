from setup.properties import *
import re

def init_audio_activity(params):

	client = params['client']
	slash = params['slash']
	discord = params['discord']
	get = params['get']
	YoutubeDL = params['YoutubeDL']
	FFmpegPCMAudio = params['FFmpegPCMAudio']


	ydl_opts = {'format': 'bestaudio/best'}
	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

	# @client.command(pass_context=True)
	@slash.slash(name = "play", description = "Play a Youtube url", guild_ids = [guildId])
	async def play(ctx, url):

		try:
			user = ctx.author
			voice = get(client.voice_clients, guild = ctx.guild)
			
			if voice == None:

				if (user.voice == None):
					await ctx.send('You need to be connected to a voice channel')
					return
				
				youtube_regex = (
					r'(https?://)?(www\.)?'
					'(youtube|youtu|youtube-nocookie)\.(com|be)/'
					'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
				youtube_regex_match = re.match(youtube_regex, url)
				if not youtube_regex_match:
					await ctx.send('You need to provide a valide youtube url')
					return
				vc = user.voice.channel

				await ctx.send(f':arrow_down: **Loading :** <{url}>')
				await vc.connect()
				voice = get(client.voice_clients, guild = ctx.guild)
				if not voice.is_playing():
					with YoutubeDL(ydl_opts) as ydl:
						info = ydl.extract_info(url, download = False)
					URL = info['formats'][0]['url']


					await ctx.send(f':musical_note: **Now playing :** <{url}>')
					voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
					
					voice.source = discord.PCMVolumeTransformer(voice.source)

			else:
				await ctx.send("I'm already connected!")
		except Exception as ex:
			print('----- /play -----')
			print(ex)

	# @client.command(pass_context=True)
	@slash.slash(name = "pause", description = "Pause current playing audio", guild_ids = [guildId])
	async def pause(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice and voice.is_playing():
				await ctx.send('⏸ Pausing ...')
				voice.pause()
			else:
				await ctx.send('❌ The bot is not playing anything at the moment')
		except Exception as ex:
			print('----- /pause -----')
			print(ex)
			
	# @client.command(pass_context=True)
	@slash.slash(name = "resume", description = "Resume current playing audio", guild_ids = [guildId])
	async def resume(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice and voice.is_paused():
				await ctx.send('▶ Resuming ...')
				voice.resume()
			else:
				await ctx.send('❌ The bot is already (or not) playing something before this')
		except Exception as ex:
			print('----- /resume -----')
			print(ex)
	
	# @client.command(pass_context=True)
	@slash.slash(name = "stop", description = "Stop current playing audio", guild_ids = [guildId])
	async def stop(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice and voice.is_playing():
				await ctx.send('⏹ Stopping ...')
				voice.stop()
				if voice != None:
					await voice.disconnect()
			else:
				await ctx.send('❌ The bot is not playing anything at the moment')
		except Exception as ex:
			print('----- /stop -----')
			print(ex)

	# # @client.command(pass_context=True)
	# @slash.slash(name = "leave", description = "Disconnect the bot from the voice room", guild_ids = [guildId])
	# async def leave(ctx):
	# 	try:
	# 		await ctx.send('Leaving ...')
	# 		voice = get(client.voice_clients, guild = ctx.guild)
	# 		if voice != None:
	# 			await voice.disconnect()
	# 	except Exception as ex:
	# 		print(ex)
