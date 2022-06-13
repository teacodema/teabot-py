from setup.data.params import *
from setup.data.properties import *
from setup.actions.common import *

def init_quran(params):
	
	bot = params['bot']
	get = params['get']
	discord = params['discord']
	slash = params['slash']
	asyncio = params['asyncio']
	YoutubeDL = params['YoutubeDL']
	PCMVolumeTransformer = params['PCMVolumeTransformer']
	ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
	}


	ffmpeg_options = {
			'options': '-vn'
	}
	ytdl = YoutubeDL(ytdl_format_options)

	class YTDLSource(PCMVolumeTransformer):
		def __init__(self, source, *, data, volume=0.5):
			super().__init__(source, volume)
			self.data = data
			self.title = data.get('title')
			self.url = data.get('url')

		@classmethod
		async def from_url(cls, url, *, loop=None, stream=False):
			loop = loop or asyncio.get_event_loop()
			data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
			filename = data['url'] if stream else ytdl.prepare_filename(data)
			return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

	@slash.slash(name = "quran", description = "Live Quran", guild_ids = [guildId])
	async def quran_live(ctx):
		
		if player_params['current_played'] == 'audio':
			await ctx.send('⚠ A track is currently playing')
			return
		player_params['current_played'] = 'quran'
		
		# link = link.lower()
		radio_url_1 = 'https://Qurango.net/radio/tarateel'
		# if link == 'short recitations':
		player = await YTDLSource.from_url(radio_url_1, loop=bot.loop, stream=True)
		
		user = ctx.author
		if user.voice == None:
			await ctx.send('❌ You need to be connected to a voice channel')
			return

		voice = get(bot.voice_clients, guild = ctx.guild)
		if voice and voice.is_connected() and (voice.is_playing() or voice.is_paused()):
			await ctx.send('⚠ A track is currently playing')
			return

		vc = user.voice.channel
		if not voice or not voice.is_connected():
			await vc.connect()
		
		voice = get(bot.voice_clients, guild = ctx.guild)
		voice.play(player)
		# ctx.voice_client.play(player)
		await ctx.send("Now playing Live **mp3quran.net radio**")