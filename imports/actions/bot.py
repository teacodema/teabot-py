
def activity_states_data(params):
    discord = params['discord']
    states = ["online", "dnd", "idle", "offline", "streaming"]
    discord_states = [ discord.Status.online, discord.Status.dnd, discord.Status.idle, discord.Status.offline, discord.Status.streaming]
    activity_types = ["watching", "listening", "playing", "streaming", "competing"]
    discord_activity_types = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing, discord.ActivityType.streaming, discord.ActivityType.competing]
    return { 
        "states": states,
        "discord_states": discord_states, 
        "activity_types": activity_types,
        "discord_activity_types": discord_activity_types
    }