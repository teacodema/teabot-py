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
        'tc_check_new_members', 'tc_update_new_members',
        'tc_toggle_role', 'tc_toggle_roles_members',
        'event_subscribers', 'event_create', 'event_edit_status', 'get_events_by_name',
        'clone_voice_channel', 'delete_voice_channel'
    ],
	'root': [
        'tc_welcome',
        'tc_hide_channel', 'tc_lock_channel', 
        'tc_thread_delete', 'tc_thread_archive',
        'tc_make_webhook', 'tc_msg_member', 'tc_msg_channel', 'tc_edit_msg_channel',
        'tc_reply_channel', 'tc_remove_msg',
        'tc_bot_react', 'tc_update_roles_reactions', 'tc_get_message_reactions',
        'tc_members_has_role', 'tc_update_roles_position', 'tc_roles_fetch',
        'event_delete_between_dates',
    ],
}
