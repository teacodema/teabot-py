from setup.properties import *
import re

def init_audio_activity(params):

	client = params['client']
	slash = params['slash']
	discord = params['discord']
	get = params['get']
	YoutubeDL = params['YoutubeDL']
	FFmpegPCMAudio = params['FFmpegPCMAudio']
	playlist = []
	currentTrackIndex = 0
	_ctxPlay = None,
	voice = None
	btn_pressed = False


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

			if (user.voice == None):
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			
			vc = user.voice.channel
			if not url:
				if len(playlist) == 0:
					await ctx.send('The playlist is empty ⚠')
					return
				if voice == None:
					await resetPlayer(ctx, "✅ Connected + Track is queued + played", None, vc)
				else:
					await ctx.send("▶ Playing ...")
					playTrack(ctx)
				return
			else:
				youtube_regex = (
					r'(https?://)?(www\.)?'
					'(youtube|youtu|youtube-nocookie)\.(com|be)/'
					'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
				youtube_regex_match = re.match(youtube_regex, url)
				if not youtube_regex_match:
					await ctx.send('❌ You need to provide a valide youtube url')
					return

			if (voice):
				if (voice.is_connected()):
					if (voice.is_playing()):
						await ctx.send("⬆ Track is queued")
						track = extrackUrlData(url)
						playlist.append(track)
					else:
						await resetPlayer(ctx, "▶ Playing ...", url)
						# await resetPlayer(ctx, "🎵 Track is queued + played", url)
				else:
					await resetPlayer(ctx, "▶ Playing ...", url, vc)
					# await resetPlayer(ctx, "🎵 Track is queued + played", url, vc)
			else:
				await resetPlayer(ctx, "▶ Playing ...", url, vc)
				# await resetPlayer(ctx, "✅ Connected + Track is queued + played", url, vc)
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
			playTrack(ctx)
		except Exception as ex:
			print('----- resetPlayer -----')
			print(ex)
	
	def playNext(err):
		try:
			nonlocal currentTrackIndex, playlist, voice, _ctxPlay, btn_pressed
			
			if btn_pressed:
				btn_pressed = False
				return
			if len(playlist) == 0:
				# await ctx.send('⚠ The playlist is empty')
				return
			voice = get(client.voice_clients, guild = _ctxPlay.guild)
			if not voice or not voice.is_connected():
				# await ctx.send('❌ The bot is not connected')
				return

			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex > len(playlist) - 1:
				currentTrackIndex = 0
			
			voice.stop()
			playTrack(_ctxPlay)
		except Exception as ex:
			print('----- playNext -----')
			print(ex)

	def playTrack(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, _ctxPlay
			_ctxPlay = ctx
			track = playlist[currentTrackIndex]
			voice = get(client.voice_clients, guild = ctx.guild)
			voice.play(FFmpegPCMAudio(track['_url'], **FFMPEG_OPTIONS), after=playNext)
		except Exception as ex:
			print('----- playTrack -----')
			print(ex)

	######################## CURRENT ########################
	@slash.slash(name = "current", description = "Shows current playing track", guild_ids = [guildId])
	async def current(ctx):
		try:
			nonlocal currentTrackIndex, playlist
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			track = playlist[currentTrackIndex]
			value = f"**{currentTrackIndex+1}・**{track['title']}"
			guild = client.get_guild(ctx.guild_id)
			embed = discord.Embed(title='TeaBot', description="", color=0x1da1f2)
			embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.add_field(name="⏳│Playing Now", value=value, inline=True)
			await ctx.send(embed=embed)
		except Exception as ex:
			print('----- /current -----')
			print(ex)


	######################## PLAYLIST ########################
	@slash.slash(name = "playlist", description = "Shows the playlist", guild_ids = [guildId])
	async def _playlist(ctx):
		try:
			nonlocal playlist
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return

			value = ""
			for i in range(len(playlist)):
				track = playlist[i]
				if (currentTrackIndex == i):
					index = '►'
				else:
					index = i+1
				value += f"**{index}・**{track['title']}\n"
			guild = client.get_guild(ctx.guild_id)
			embed = discord.Embed(title='TeaBot', description="", color=0x1da1f2)
			embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.add_field(name="📋│Playlist", value=value, inline=True)
			await ctx.send(embed=embed)
		except Exception as ex:
			print('----- /playlist -----')
			print(ex)

	######################## PLAYLIST ########################
	@slash.slash(name = "flushlist", description = "Flushes the playlist", guild_ids = [guildId])
	async def flushlist(ctx):
		try:
			nonlocal playlist
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
				await ctx.send('⚠ A track is currently playing')
				return
			playlist = []
			await ctx.send('🗑 Playlist is clear')
		except Exception as ex:
			print('----- /flushlist -----')
			print(ex)


	######################## NEXT ########################
	@slash.slash(name = "next", description = "Play next track", guild_ids = [guildId])
	async def next(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			btn_pressed = True
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏭ Next ...')
			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex >= len(playlist):
				currentTrackIndex = 0

			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			playTrack(ctx)
		except Exception as ex:
			print('----- /next -----')
			print(ex)

	######################## PREVIOUS ########################
	@slash.slash(name = "previous", description = "Play previous track", guild_ids = [guildId])
	async def previous(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			btn_pressed = True
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏮ Previous ...')
			currentTrackIndex = currentTrackIndex - 1
			if currentTrackIndex < 0:
				currentTrackIndex = len(playlist) - 1

			voice = get(client.voice_clients, guild = ctx.guild)
			voice.stop()
			playTrack(ctx)
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
				await ctx.send('⏯ Resuming ...')
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
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			btn_pressed = True			
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
			voice = get(client.voice_clients, guild = ctx.guild)
			if voice != None:
				await voice.disconnect()
				await ctx.send('🚪 Leaving ...')
			else:
				await ctx.send('❌ Not connected ...')
		except Exception as ex:
			print('----- /leave -----')
			print(ex)
