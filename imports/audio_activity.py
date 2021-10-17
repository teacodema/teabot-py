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
	currentTrackIndex = 0
	skipCmdClicked = False


	ydl_opts = {'noplaylist': True,
        			'outtmpl': 'music',
							'format': 'bestaudio/best',
							'postprocessors': [{
									'key': 'FFmpegExtractAudio',
									'preferredcodec': 'mp3',
									'preferredquality': '128',
							}]}
	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

	######################## PLAY ########################
	@slash.slash(name = "play", description = "Play a Youtube url", guild_ids = [guildId])
	async def play(ctx, url=None):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			user = ctx.author
			voice = get(client.voice_clients, guild = ctx.guild)
			vc = user.voice.channel

			if (user.voice == None):
				await ctx.send('You need to be connected to a voice channel')
				return
			
			if url:
				youtube_regex = (
					r'(https?://)?(www\.)?'
					'(youtube|youtu|youtube-nocookie)\.(com|be)/'
					'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
				youtube_regex_match = re.match(youtube_regex, url)
				if not youtube_regex_match:
					await ctx.send('You need to provide a valide youtube url')
					return
			else:
				if len(playlist) == 0:
					await ctx.send('The playlist is empty ⚠')
					return
				await playTrack(ctx)
				if voice == None:
					await resetPlayer(ctx, "✅ Connected + Track is queued + played", None, vc)
				return

			if (voice):
				if (voice.is_connected()):
					if (voice.is_playing()):
						await ctx.send("⬆ Track is queued")
						track = extrackUrlData(url)
						playlist.append(track)
					else:
						await resetPlayer(ctx, "🎵 Track is queued + played", url)
				else:
					await resetPlayer(ctx, "🎵 Track is queued + played", url, vc)
			else:
				await resetPlayer(ctx, "✅ Connected + Track is queued + played", url, vc)
		except Exception as ex:
			print('----- /play -----')
			print(ex)

	def extrackUrlData(url):
		nonlocal ydl_opts
		with YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url, download = False)
		URL = info['formats'][0]['url']
		title = info['title']
		duration = info['duration']
		return {"_url": URL, "url": url, "title": title, "duration": duration}

	async def resetPlayer(ctx, msg, url=None, vc=None):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			await ctx.send(msg)
			if url:
				# playlist = []
				track = extrackUrlData(url)
				playlist.append(track)
			else:
				track = playlist[currentTrackIndex]
			currentTrackIndex = 0
			if vc:
				await vc.connect()
			await playTrack(ctx)
		except Exception as ex:
			print('----- resetPlayer -----')
			print(ex)
		

	async def playTrack(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, skipCmdClicked

			track = playlist[currentTrackIndex]
			await ctx.send(f'▶ **Playing ** __{track["title"]}__')
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.play(FFmpegPCMAudio(track['_url'], **FFMPEG_OPTIONS))

			duration = track['duration']
			print(f'task made {duration}')
			@tasks.loop(seconds=duration, count=2, reconnect=None)
			async def toNextTrack(duration):
				try:
					nonlocal currentTrackIndex, playlist, skipCmdClicked
					if toNextTrack.current_loop != 0:
						print(f'task done {duration}')
						print(f'skip: {skipCmdClicked}, index: {currentTrackIndex}')
						if skipCmdClicked:
							skipCmdClicked = False
							return
						if len(playlist) == 0:
							# await ctx.send('⚠ The playlist is empty')
							return
						voice = get(client.voice_clients, guild = ctx.guild)
						if not voice or not voice.is_connected():
							# await ctx.send('❌ The bot is not connected')
							return

						if currentTrackIndex >= len(playlist) - 1:
							currentTrackIndex = -1
						currentTrackIndex = currentTrackIndex + 1
						voice.stop()
						await playTrack(ctx)
				except Exception as ex:
					print('----- toNextTrack_loop -----')
					print(ex)
			toNextTrack.start(duration)
		except Exception as ex:
			print('----- playTrack -----')
			print(ex)



	######################## PLAYLIST ########################
	@slash.slash(name = "playlist", description = "Shows the playlist", guild_ids = [guildId])
	async def _playlist(ctx):
		try:
			nonlocal playlist
			value = ""
			# for track in playlist:
			if len(playlist):
				for i in range(len(playlist)):
					track = playlist[i]
					value += f"**{i+1}**・{track['title']}\n"
				embed = discord.Embed(title='TeaBot', description="", color=0x1da1f2)
				embed.add_field(name="📋・Playlist", value=value, inline=True)
				await ctx.send(embed=embed)
			else:
				await ctx.send('⚠ The playlist is empty')
		except Exception as ex:
			print('----- /playlist -----')
			raise ex
			print(ex)

	######################## NEXT ########################
	@slash.slash(name = "next", description = "Play next track", guild_ids = [guildId])
	async def next(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, skipCmdClicked
			skipCmdClicked = True
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏭ Next ...')
			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex >= len(playlist):
				currentTrackIndex = 0
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			await playTrack(ctx)
		except Exception as ex:
			print('----- /next -----')
			print(ex)

	######################## PREVIOUS ########################
	@slash.slash(name = "previous", description = "Play previous track", guild_ids = [guildId])
	async def previous(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, skipCmdClicked
			skipCmdClicked = True
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏮ Previous ...')
			currentTrackIndex = currentTrackIndex - 1
			if currentTrackIndex < 0:
				currentTrackIndex = len(playlist) - 1
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			await playTrack(ctx)
		except Exception as ex:
			print('----- /previous -----')
			print(ex)

	######################## PAUSE ########################
	@slash.slash(name = "pause", description = "Pauses the player", guild_ids = [guildId])
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
	@slash.slash(name = "resume", description = "Resumes the player", guild_ids = [guildId])
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
	@slash.slash(name = "stop", description = "Stops the player", guild_ids = [guildId])
	async def stop(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice:
				if voice.is_playing() or voice.is_connected():
					await ctx.send('⏹ Stopping ...')
					voice.stop()
			else:
				await ctx.send('❌ The bot is not playing anything at the moment')
		except Exception as ex:
			print('----- /stop -----')
			print(ex)

	######################## LEAVE ########################
	@slash.slash(name = "leave", description = "Disconnect the bot from the voice room", guild_ids = [guildId])
	async def leave(ctx):
		try:
			await ctx.send('Leaving ...')
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice != None:
				await voice.disconnect()
		except Exception as ex:
			print(ex)
