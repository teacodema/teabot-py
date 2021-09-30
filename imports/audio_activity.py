from setup.properties import *


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
	async def play(ctx, url = None, volume: int = 10):

		try:
			user = ctx.author
			voice = get(client.voice_clients, guild = ctx.guild)
			
			if voice == None:
				
				if (url == None):
					await ctx.send('You need to provide a valide youtube url')
					return
				if (user.voice == None):
					await ctx.send('You need to be connected to a voice channel')
					return
				vc = user.voice.channel

				await ctx.send(f':arrow_down: **Loading :** <{url}>')
				await vc.connect()
				voice = get(client.voice_clients, guild = ctx.guild)
				if not voice.is_playing():
					with YoutubeDL(ydl_opts) as ydl:
						info = ydl.extract_info(url, download = False)
					URL = info['formats'][0]['url']
					# voice.volume = 0 #Not working

					# voice.source.volume = 0.1
					# await ctx.send(f"Joining ...")

					await ctx.send(f':musical_note: **Now playing :** <{url}>')
					voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
					# voice.is_playing()
					
					voice.source = discord.PCMVolumeTransformer(voice.source)
					# voice.source.volume = float(volume)

					try:
						voice.source.volume = volume/100
					except:
						voice.source.volume = 0.1
			else:
				await ctx.send("I'm already connected!")
		except Exception as ex:
			print(ex)

	# @client.command(pass_context=True)
	@slash.slash(name = "pause", description = "Pause current playing audio", guild_ids = [guildId])
	async def pause(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice.is_playing():
				await ctx.send('Pausing ...')
				voice.pause()
			else:
				await ctx.send('❌ The bot is not playing anything at the moment')
		except Exception as ex:
			print(ex)
			
	# @client.command(pass_context=True)
	@slash.slash(name = "resume", description = "Resume current playing audio", guild_ids = [guildId])
	async def resume(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice.is_paused():
				await ctx.send('Resuming ...')
				voice.resume()
			else:
				await ctx.send('❌ The bot was not playing anything before this')
		except Exception as ex:
			print(ex)
	
	# @client.command(pass_context=True)
	@slash.slash(name = "stop", description = "Stop current playing audio", guild_ids = [guildId])
	async def stop(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice.is_playing():
				await ctx.send('Stopping ...')
				voice.stop()
			else:
				await ctx.send('The bot is not playing anything at the moment')
		except Exception as ex:
			print(ex)

	# @client.command(pass_context=True)
	@slash.slash(name = "leave", description = "Disconnect the bot from the voice room", guild_ids = [guildId])
	async def leave(ctx):
		try:
			await ctx.send('Leaving ...')
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice != None:
				await voice.disconnect()
		except Exception as ex:
			print(ex)
