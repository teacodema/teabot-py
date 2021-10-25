from setup.properties import *
import re
import datetime
import random

def init_audio_activity(params):

	bot = params['bot']
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

	ydl_opts = {
							'noplaylist': True,
			        'nocheckcertificate': True,
							'max-downloads': 1,
        			'outtmpl': 'music',
							'format': 'bestaudio/best',
			        'audioformat': 'mp3',
							# 'ignoreerrors': True,
							'no_warnings': True,
							'quiet': True,
							'postprocessors': [{
									'key': 'FFmpegExtractAudio',
									'preferredcodec': 'mp3',
									'preferredquality': '128',
							}]}
	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
		'options': '-vn'}

	######################## PLAY ########################
	@slash.slash(name = "play", description = "Play a Youtube url", guild_ids = [guildId])
	async def play(ctx, url=None):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			# user = ctx.author

			# if (user.voice == None):
			# 	await ctx.send('❌ You need to be connected to a voice channel')
			# 	return
			
			# vc = user.voice.channel
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not url:
				if len(playlist) == 0:
					await ctx.send('⚠ The playlist is empty')
					return
				if voice == None:
					await Player(ctx, "▶ Playing ...", None, vc)
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
					await ctx.send('❌ You need to provide a valide youtube video url')
					return

			if (voice):
				if (voice.is_connected()):
					if (voice.is_playing() or voice.is_paused()):
						await ctx.send("⬆ Track is queued")
						track = extractUrlData(url)
						playlist.append(track)
					else:
						await Player(ctx, "▶ Playing ...", url)
				else:
					await Player(ctx, "▶ Playing ...", url, vc)
			else:
				await Player(ctx, "▶ Playing ...", url, vc)
		except Exception as ex:
			print('----- /play -----')
			print(ex)

	def extractUrlData(url):
		try:
			nonlocal ydl_opts
			with YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(url, download = False)
			URL = info['formats'][0]['url']
			title = info['title']
			duration = info['duration']
			thumbnail = info['thumbnail']
			id = info['id']
			track = {
				"_url": URL, "url": url,
				"id": id, "title": title,
				"_duration": duration, "duration": str(datetime.timedelta(seconds=duration)).lstrip("0:"),
				"thumbnail": thumbnail
			}
			return track
		except Exception as ex:
			print('----- extractUrlData -----')
			print(ex)


	async def Player(ctx, msg = None, url=None, vc=None):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts
			if msg:
				await ctx.send(msg)
			if url:
				# playlist = []
				track = extractUrlData(url)
				playlist.append(track)
				currentTrackIndex = len(playlist) - 1 #0
			else:
				currentTrackIndex = 0
				track = playlist[currentTrackIndex]

			voice = get(bot.voice_clients, guild = ctx.guild)
			if vc and (not voice or not voice.is_connected()):
				await vc.connect()
			playTrack(ctx)
		except Exception as ex:
			print('----- Player -----')
			print(ex)
	
	def playNext(err):
		try:
			nonlocal currentTrackIndex, playlist, voice, _ctxPlay, btn_pressed
			
			print(err)

			if btn_pressed:
				btn_pressed = False
				return
			if len(playlist) == 0:
				# await ctx.send('⚠ The playlist is empty')
				return
			voice = get(bot.voice_clients, guild = _ctxPlay.guild)
			if not voice or not voice.is_connected():
				# await ctx.send('❌ The bot is not connected')
				return

			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex > len(playlist) - 1:
				currentTrackIndex = 0
			
			# voice.stop()
			playTrack(_ctxPlay)
		except Exception as ex:
			print('----- playNext -----')
			print(ex)

	def playTrack(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, _ctxPlay, btn_pressed
			btn_pressed = True
			_ctxPlay = ctx
			track = playlist[currentTrackIndex]
			voice = get(bot.voice_clients, guild = ctx.guild)
			voice.stop()
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
			value = f"**{currentTrackIndex+1}・**{track['title']} - {track['duration']}"
			guild = bot.get_guild(ctx.guild_id)
			embed = discord.Embed(color=0x1da1f2)
			embed.set_thumbnail(url=track['thumbnail'])
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			# embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
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

			await displayPlaylist(ctx)
		except Exception as ex:
			print('----- /playlist -----')
			print(ex)

	######################## REPLAY ########################
	@slash.slash(name = "replay", description = "Replay current track", guild_ids = [guildId])
	async def replay(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			btn_pressed = True
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('▶ Replay ...')

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not voice or not voice.is_connected():
				await vc.connect()
			playTrack(ctx)
		except Exception as ex:
			print('----- /replay -----')
			print(ex)

	######################## NEXT ########################
	@slash.slash(name = "next", description = "Play next track", guild_ids = [guildId])
	async def next(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			btn_pressed = True
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏭ Next ...')
			currentTrackIndex = currentTrackIndex + 1
			if currentTrackIndex >= len(playlist):
				currentTrackIndex = 0

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not voice or not voice.is_connected():
				await vc.connect()
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
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The playlist is empty')
				return
			await ctx.send('⏮ Previous ...')
			currentTrackIndex = currentTrackIndex - 1
			if currentTrackIndex < 0:
				currentTrackIndex = len(playlist) - 1

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not voice or not voice.is_connected():
				await vc.connect()
			playTrack(ctx)
		except Exception as ex:
			print('----- /previous -----')
			print(ex)

	######################## PAUSE ########################
	@slash.slash(name = "pause", description = "Pauses the player", guild_ids = [guildId])
	async def pause(ctx):
		try:
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			voice = get(bot.voice_clients, guild = ctx.guild)
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
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			voice = get(bot.voice_clients, guild = ctx.guild)
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
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice and (voice.is_playing() or voice.is_paused()):
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
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice != None:
				await voice.disconnect()
				await ctx.send('🚪 Leaving ...')
			else:
				await ctx.send('❌ Not connected ...')
		except Exception as ex:
			print('----- /leave -----')
			print(ex)

	######################## CLEAR PLAYLIST ########################
	@slash.slash(name = "clear-list", description = "Flushes the playlist", guild_ids = [guildId])
	async def clear_list(ctx):
		try:
			nonlocal playlist
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
				await ctx.send('⚠ A track is currently playing')
				return
			playlist = []
			await ctx.send('🗑 Playlist is clear')
		except Exception as ex:
			print('----- /flushlist -----')
			print(ex)

	######################## REFRESH LIST ########################
	@slash.slash(name = "refresh", description = "Refill the playlist with some tracks", guild_ids = [guildId])
	async def refresh(ctx):
		try:
			nonlocal playlist
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
				await ctx.send('⚠ A track is currently playing')
				return
			playlist = []
			await ctx.send('📋 Processing ... just a moment')
			initPlaylist()
			await displayPlaylist(ctx)
		except Exception as ex:
			print('----- /refresh -----')
			print(ex)
	
	def isUserConnected(ctx):
		try:
			user = ctx.author
			# voice = get(client.voice_clients, guild = ctx.guild)
			if user.voice == None:
				# await ctx.send('❌ You need to be connected to a voice channel')
				return False
			vc = user.voice.channel
			return vc
		except Exception as ex:
			print('----- checkUserVoice -----')
			print(ex)
			return False
	
	async def displayPlaylist(ctx):
		try:
			nonlocal playlist, currentTrackIndex
			value = ""
			for i in range(len(playlist)):
				track = playlist[i]
				if (currentTrackIndex == i):
					index = '►'
				else:
					index = i+1
				# track_title = track['title'][0:40]
				# track_title = track_title.replace("[", "\(")
				# track_title = track_title.replace("]", "\)")
				# track_url = track['url']
				# track_url = track_url.replace("(", "\(")
				# track_url = track_url.replace(")", "\)")
				value += f"**{index}・**{track['title'][0:40]}... - {track['duration']}\n"
			guild = bot.get_guild(ctx.guild_id)
			embed = discord.Embed(color=0x1da1f2)
			# embed.set_thumbnail(url=guild.icon_url)
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			# embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.add_field(name="📋│Playlist", value=value, inline=True)
			await ctx.send(embed=embed)
		except Exception as ex:
			print('----- displayPlaylist -----')
			print(ex)

	def initPlaylist():
		try:
			nonlocal playlist
			defaultList = [
				'https://www.youtube.com/watch?v=EM1cCc0Kphk',	#Zulishanti - Likwid (Sauniks Remix)
				'https://www.youtube.com/watch?v=wOO_5Mv1JXQ',	#Zubi - Sugar (feat. Anatu)
				'https://www.youtube.com/watch?v=bX4C8B2MEak',	#DIOR, Samo & ID - Положение | Так дайте пацанам посчитать потери
				'https://www.youtube.com/watch?v=mbnjzSFuU8Y',	#Zeraphym - Lifeline
				'https://www.youtube.com/watch?v=qAgPH1CWiAw',	#Attack on Titan 2 - 'Barricades' with Lyrics
				'https://www.youtube.com/watch?v=HHgepB44oMk',	#X-Ray Dog - Prophet [HQ]
				'https://www.youtube.com/watch?v=bLZHcnuqscU',	#Unknown Brain x Rival - Control (feat. Jex) [NCS Release]
				'https://www.youtube.com/watch?v=yJg-Y5byMMw',	#Warriyo - Mortals (feat. Laura Brehm) [NCS Release]
				'https://www.youtube.com/watch?v=BnSkt6V3qF0', 	#Ruelle - Madness
				'https://www.youtube.com/watch?v=FA2w-PMKspo',	#Thirty Seconds To Mars - Walk On Water (Lyric Video)
				'https://www.youtube.com/watch?v=VDvr08sCPOc',	#Remember The Name (Official Video) - Fort Minor
				'https://www.youtube.com/watch?v=qaX5nR2GFaY', 	#Leon Machère & Kay One - Portofino 🌴☀️ ft. Tilly (Official Video)
				'https://www.youtube.com/watch?v=8Hu8L7psTHQ', 	#GIMS - Miami Vice (Clip Officiel)
				'https://www.youtube.com/watch?v=MTmUmU7LaHg',	#GIMS - Jasmine (Audio Officiel)
				'https://www.youtube.com/watch?v=GpkHJlyV7TQ',	#Feint - My Sunset (Original Mix)

			]
			random.shuffle(defaultList)
			defaultList = defaultList[0:3]

			for track_url in defaultList:
				track = extractUrlData(track_url)
				playlist.append(track)
		except Exception as ex:
			print('----- initPlaylist -----')
			print(ex)
				
	initPlaylist()
