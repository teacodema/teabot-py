from setup.properties import *
import re

def init_audio_activity(params):

	client = params['client']
	slash = params['slash']
	discord = params['discord']
	get = params['get']
	YoutubeDL = params['YoutubeDL']
	FFmpegPCMAudio = params['FFmpegPCMAudio']
	tasks = params['tasks']
	playlist = []
	currentTrackIndex = -1


	ydl_opts = {'format': 'bestaudio/best'}
	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

	######################## PLAY ########################
	@slash.slash(name = "play", description = "Play a Youtube url", guild_ids = [guildId])
	async def play(ctx, url):

		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			user = ctx.author
			voice = get(client.voice_clients, guild = ctx.guild)

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

			if (voice):
				if (voice.is_connected()):
					if (voice.is_playing()):
						playlist.append(url)
						await ctx.send("1 Track is queued")
					else:
						await resetPlayer(ctx, ydl_opts, url, "2 Track is queued + played")
				else:
					await resetPlayer(ctx, ydl_opts, url, "3 Track is queued + played", vc)
			else:
				await resetPlayer(ctx, ydl_opts, url, "4 connect + Track is queued + played", vc)
		except Exception as ex:
			print('----- /play -----')
			print(ex)

	async def resetPlayer(ctx, ydl_opts, url, msg, vc=None):
		try:
			nonlocal currentTrackIndex, playlist
			playlist = []
			playlist.append(url)
			currentTrackIndex = 0
			if vc:
				await vc.connect()
			voice = get(client.voice_clients, guild = ctx.guild)
			await playTrack(ctx, currentTrackIndex, voice, ydl_opts)
			await ctx.send(msg)
		except Exception as ex:
			print('----- resetPlayer -----')
			print(ex)
		

	async def playTrack(ctx, index, voice, ydl_opts):
		try:
			nonlocal currentTrackIndex, playlist

			print(f'index : {index}')
			print(f'length : {len(playlist)}')

			url = playlist[index]
			with YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(url, download = False)
			URL = info['formats'][0]['url']
			await ctx.send(f':musical_note: **Now playing :** <{url}>')
			voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

			if index == len(playlist) - 1:
				duration = info['duration']
				@tasks.loop(seconds=duration, count=2, reconnect=True)
				async def toNextTrack():
					try:
						nonlocal currentTrackIndex, playlist
						if toNextTrack.current_loop != 0:
							currentTrackIndex = currentTrackIndex + 1
							voice.stop()
							await playTrack(ctx, currentTrackIndex, voice, ydl_opts)
					except Exception as ex:
						print('----- toNextTrack_loop -----')
						print(ex)
				toNextTrack.start()
		except Exception as ex:
			print('----- playTrack -----')
			print(ex)


	######################## NEXT ########################
	@slash.slash(name = "next", description = "Play next audio", guild_ids = [guildId])
	async def next(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			if len(playlist) == 0:
				await ctx.send('The playlist is empty ⚠')
				return
			
			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex >= len(playlist):
				currentTrackIndex = 0
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			await playTrack(ctx, currentTrackIndex, voice, ydl_opts)

		except Exception as ex:
			print('----- /next -----')
			print(ex)

	######################## PREVIOUS ########################
	@slash.slash(name = "previous", description = "Play previous audio", guild_ids = [guildId])
	async def previous(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			if len(playlist) == 0:
				await ctx.send('The playlist is empty ⚠')
				return
			
			currentTrackIndex = currentTrackIndex - 1
			if currentTrackIndex < 0:
				currentTrackIndex = len(playlist) - 1
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			await playTrack(ctx, currentTrackIndex, voice, ydl_opts)

		except Exception as ex:
			print('----- /previous -----')
			print(ex)

	######################## PAUSE ########################
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
			
	######################## RESUME ########################
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
	
	######################## STOP ########################
	@slash.slash(name = "stop", description = "Stop current playing audio", guild_ids = [guildId])
	async def stop(ctx):
		try:
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice:
				if voice.is_playing() or voice.is_connected():
					await ctx.send('⏹ Stopping ...')
					voice.stop()
					await voice.disconnect()
			else:
				await ctx.send('❌ The bot is not playing anything at the moment')
		except Exception as ex:
			print('----- /stop -----')
			print(ex)
