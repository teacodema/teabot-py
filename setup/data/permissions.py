functions_roles = {
    '*': [
        'server_info', 'role_info', 'member_info',
        'janken', 'pick_speaker',
        'tag',
        'play', 'replay', 'pause', 'resume', 'previous', 'next', 'stop'
        'track', 'queue', 'clear-queue', 'refresh', 'leave',
    ],
    'staff': [
        'purge',
        'check_new_members', 'update_new_members',
        'toggle_role', 'toggle_role_members',
        'event_subscribers', 'event_create',
        'clone_voice_channel', 'delete_voice_channel'
    ],
	'root': [
        'welcome', 'check_new_members', 'update_new_members',
        'make_webhook', 'msg_member', 'msg_channel', 'edit_msg_channel',
        'reply_channel', 'remove_msg_member', 'purge',
        'bot_react', 'get_message_reactions',
        'toggle_role', 'toggle_role_members', 'members_has_role', 'update_roles',
        'event_subscribers', 'event_delete_between_dates', 'event_create',
        'clone_voice_channel', 'delete_voice_channel',
    ],
}
