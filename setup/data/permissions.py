functions_roles = {
    '*': [
        'server_info', 'role_info', 'member_info',
        'janken',
        'tag_rules',
        'play', 'replay', 'pause', 'resume', 'previous', 'next', 'stop'
        'track', 'queue', 'clear-queue', 'refresh', 'leave',
    ],
    'hosts': [
        'pick_speaker',
    ],
    'staff': [
        'purge',
        'pick_speaker', 'poll',
        'check_new_members', 'update_new_members',
        'toggle_role', 'toggle_roles_members',
        'event_subscribers', 'event_create',
        'clone_voice_channel', 'delete_voice_channel'
    ],
	'root': [
        'welcome',
        'hide_channel', 'lock_channel', 
        'delete_threads',
        'make_webhook', 'msg_member', 'msg_channel', 'edit_msg_channel',
        'reply_channel', 'remove_msg_member',
        'bot_react', 'update_roles_reactions', 'get_message_reactions',
        'members_has_role', 'update_roles_position',
        'event_delete_between_dates',
    ],
}
