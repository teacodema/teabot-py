functions_roles = {
    '*': [
        'tag',
        'play', 'replay', 'pause', 'resume', 'previous', 'next', 'stop'
        'track', 'queue', 'clear-queue', 'refresh', 'leave',
    ],
    'staff': [
        'purge', 'event_create',
    ],
	'root': [
        'server_info', 'role_info', 'member_info',
        'welcome', 'check_new_members', 'update_new_members',
        'make_webhook', 'msg_member', 'msg_channel', 'edit_msg_channel',
        'reply_channel', 'remove_msg_member', 'purge', 'tag',
        'bot_react', 'toggle_role', 'toggle_role_members', 'members_has_role',
        'event_subscribers', 'event_delete_between_dates', 'event_create',
    ],
}
