functions_roles = {
    '*': [
        'server_info', 'role_info', 'member_info',
        'janken',
        'tag',
        'play', 'replay', 'pause', 'resume', 'previous', 'next', 'stop'
        'track', 'queue', 'clear-queue', 'refresh', 'leave',
    ],
    'hosts': [
        'pick_speaker'
    ],
    'staff': [
        'purge',
        'pick_speaker'
        'check_new_members', 'update_new_members',
        'toggle_role', 'toggle_role_members',
        'event_subscribers', 'event_create',
        'clone_voice_channel', 'delete_voice_channel'
    ],
	'root': [
        'welcome',
        'make_webhook', 'msg_member', 'msg_channel', 'edit_msg_channel',
        'reply_channel', 'remove_msg_member',
        'bot_react', 'get_message_reactions',
        'members_has_role', 'update_roles',
        'event_delete_between_dates',
    ],
}
