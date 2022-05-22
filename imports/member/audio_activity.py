# from database.player import *
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
	@slash.slash(name = "play", description = "Play a YouTube url", guild_ids = [guildId])
	async def play(ctx, url=None):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts

			# if player_params['current_played'] == 'quran':
			# 	await ctx.send('⚠ Quran is currently played')
			# 	return
			# player_params['current_played'] = 'audio'

			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not url:
				if len(playlist) == 0:
					await ctx.send('⚠ The queue is empty')
					return
				if voice == None:
					await Player(ctx, "▶ Playing ...", None, vc)
				elif voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
					await ctx.send('⚠ A track is currently playing')
					return
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
			print('----- /play() -----')
			print(ex)
			await log_exception(ex, '/play', ctx)

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
			print('----- extractUrlData() -----')
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
			print('----- Player() -----')
			print(ex)
			await log_exception(ex, 'Player()', ctx)
	
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
			print('----- playNext() -----')
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
			print('----- playTrack() -----')
			print(ex)

	######################## CURRENT ########################
	@slash.slash(name = "track", description = "Show current playing track", guild_ids = [guildId])
	async def current_track(ctx):
		try:
			nonlocal currentTrackIndex, playlist
			if len(playlist) == 0:
				await ctx.send('⚠ The queue is empty')
				return
			track = playlist[currentTrackIndex]
			title = track['title'][0:40]
			ar_regex = (r'[a-zA-Z]+')
			ar_regex_match = not re.match(ar_regex, title)
			if ar_regex_match:
				value = f"{track['duration']} - ...{title}**・{currentTrackIndex+1}**"
			else:
				value = f"**{currentTrackIndex+1}・**{title}... - {track['duration']}"
			# guild = bot.get_guild(ctx.guild_id)
			embed = discord.Embed(color=appParams['blue'])
			embed.set_thumbnail(url=track['thumbnail'])
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			# embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.add_field(name="⏳│Playing Now", value=value, inline=True)
			await ctx.send(embed=embed)
		except Exception as ex:
			print('----- /current_track() -----')
			print(ex)
			await log_exception(ex, '/current_track', ctx)


	######################## PLAYLIST ########################
	@slash.slash(name = "queue", description = "Show the queue", guild_ids = [guildId])
	async def queue(ctx):
		try:
			nonlocal playlist
			if len(playlist) == 0:
				await ctx.send('⚠ The queue is empty')
				return

			await displayPlaylist(ctx)
		except Exception as ex:
			print('----- /queue() -----')
			print(ex)
			await log_exception(ex, '/queue', ctx)

	######################## REPLAY ########################
	@slash.slash(name = "replay", description = "Replay current track", guild_ids = [guildId])
	async def replay(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed
			
			# if player_params['current_played'] == 'quran':
			# 	await ctx.send('⚠ Quran is currently played')
			# 	return

			btn_pressed = True
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The queue is empty')
				return
			await ctx.send('▶ Replay ...')

			voice = get(bot.voice_clients, guild = ctx.guild)
			if not voice or not voice.is_connected():
				await vc.connect()
			playTrack(ctx)
		except Exception as ex:
			print('----- /replay() -----')
			print(ex)
			await log_exception(ex, '/replay', ctx)

	######################## NEXT ########################
	@slash.slash(name = "next", description = "Play next track", guild_ids = [guildId])
	async def next(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed
			
			# if player_params['current_played'] == 'quran':
			# 	await ctx.send('⚠ Quran is currently played')
			# 	return
				
			btn_pressed = True
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The queue is empty')
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
			print('----- /next() -----')
			print(ex)
			await log_exception(ex, '/next', ctx)

	######################## PREVIOUS ########################
	@slash.slash(name = "previous", description = "Play previous track", guild_ids = [guildId])
	async def previous(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed
			
			# if player_params['current_played'] == 'quran':
			# 	await ctx.send('⚠ Quran is currently played')
			# 	return
				
			btn_pressed = True
			vc = isUserConnected(ctx)
			if vc == False:
				await ctx.send('❌ You need to be connected to a voice channel')
				return
			if len(playlist) == 0:
				await ctx.send('⚠ The queue is empty')
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
			print('----- /previous() -----')
			print(ex)
			await log_exception(ex, '/previous', ctx)

	######################## PAUSE ########################
	@slash.slash(name = "pause", description = "Pause the player", guild_ids = [guildId])
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
			print('----- /pause() -----')
			print(ex)
			await log_exception(ex, '/pause', ctx)

	######################## RESUME ########################
	@slash.slash(name = "resume", description = "Resume the player", guild_ids = [guildId])
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
			print('----- /resume() -----')
			print(ex)
			await log_exception(ex, '/resume', ctx)

	######################## STOP ########################
	@slash.slash(name = "stop", description = "Stop the player", guild_ids = [guildId])
	async def stop(ctx):
		try:
			nonlocal currentTrackIndex, playlist, ydl_opts, btn_pressed

			# player_params['current_played'] = None
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
			print('----- /stop() -----')
			print(ex)
			await log_exception(ex, '/stop', ctx)

	######################## LEAVE ########################
	@slash.slash(name = "leave", description = "Disconnect the bot from the voice room", guild_ids = [guildId])
	async def leave(ctx):
		try:
			# player_params['current_played'] = None
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice != None:
				await voice.disconnect()
				await ctx.send('🚪 Leaving ...')
			else:
				await ctx.send('❌ Not connected ...')
		except Exception as ex:
			print('----- /leave() -----')
			print(ex)
			await log_exception(ex, '/leave', ctx)

	######################## CLEAR PLAYLIST ########################
	@slash.slash(name = "clear-queue", description = "Flushes the queue", guild_ids = [guildId])
	async def clear_queue(ctx):
		try:
			nonlocal playlist
			voice = get(bot.voice_clients, guild = ctx.guild)
			if voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
				await ctx.send('⚠ A track is currently playing')
				return
			playlist = []
			await ctx.send('🗑 Queue is clear')
		except Exception as ex:
			print('----- /clear_queue() -----')
			print(ex)
			await log_exception(ex, '/clear-queue', ctx)

	######################## REFRESH LIST ########################
	@slash.slash(name = "refresh", description = "Refill the queue with some tracks", guild_ids = [guildId])
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
			print('----- /refresh() -----')
			print(ex)
			await log_exception(ex, '/refresh', ctx)
	
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
			print('----- isUserConnected() -----')
			print(ex)
			return False
	
	async def displayPlaylist(ctx):
		try:
			nonlocal playlist, currentTrackIndex
			# guild = bot.get_guild(ctx.guild_id)
			embed = discord.Embed(color=appParams['blue'])
			# embed.set_thumbnail(url=guild.icon_url)
			embed.set_footer(text=f"🌐 Visit teacode.ma")
			# embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
			embed.add_field(name="📋│Playlist", value=f'{len(playlist)} songs', inline=False)
			
			for i in range(len(playlist)):
				value = ""
				track = playlist[i]
				if (currentTrackIndex == i):
					index = '▷ Now Playing' #'►'
				else:
					index = f'✧ Song {i+1}'
				title = track['title'][0:40]
				ar_regex = (r'[a-zA-Z]+')
				ar_regex_match = not re.match(ar_regex, title)
				if ar_regex_match:
					value += f"{track['duration']} - ...{title}\n"
				else:
					value += f"{title}... - {track['duration']}\n"
				embed.add_field(name=f'{index}', value=value, inline=False)

			await ctx.send(embed=embed)
		except Exception as ex:
			print('----- displayPlaylist() -----')
			print(ex)

	def initPlaylist():
		try:
			nonlocal playlist
			defaultList = [
				'https://www.youtube.com/watch?v=5XiqmLYwsN8', #Beautiful recitation By Abbadi Houssem Eddine I Surah Yusuf
				'https://www.youtube.com/watch?v=cvV_CQo_xIk', #سورة يس الرحمن الملك الواقعة الصافات بصوت القارئ إسلام صبحي رابط بدون اعلانات
				'https://www.youtube.com/watch?v=KzG21buIJPg', #Surah Al Baqarah - Sheikh Mansour As Salimi الشيخ منصور السالمي
				'https://www.youtube.com/watch?v=S4ERCYFR28U', #سورة الملك - تبارك - كامله تلاوة هادئة قبل النوم💚تريح الاعصاب😴القرآن الكريم راحة لقلبك Surat Al Mulk
				'https://www.youtube.com/watch?v=hwB938b9ifw', #Beautiful 10 Hours of Quran Recitation by Hazaa Al Belushi
				'https://www.youtube.com/watch?v=9CN-31h_wK4', #ترتيل جميل للقارئ رعد محمد الکردي - سورة المؤمنون كاملة HD 1080
				'https://www.youtube.com/watch?v=4TK0UrGlLyo', #Sherif Mostafa | the most Beautiful recitation
				# 'https://www.youtube.com/watch?v=Axu2l8yX-aQ', #أحمد خضر سورة طه
			]
			random.shuffle(defaultList)
			defaultList = defaultList[0:3]

			for track_url in defaultList:
				try:
					track = extractUrlData(track_url)
					playlist.append(track)
				except Exception as ex:
					print(track_url)
					print(ex)
		except Exception as ex:
			print('----- initPlaylist() -----')
			print(ex)
				
	# initPlaylist()
