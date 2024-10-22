slash_commands_permissions = {
    'members': [
        'info', 'info server', 'info role', 'info member',
        'fun', 'fun janken',
        'guide', 'guide tag-rule',
        'community', 'community interview', 'community suggest',
    ],
    'hosts': [
        'member', 'member pick-speaker',
        'event', 'event create', 'event update-status'
    ],
    'staff': [
        'message', 'message purge', 'message poll',
        'member', 'member pick-speaker',
        'role', 'role toggle', 'role toggle-multiple',
        'event' 'event subscribers', 'event create',
        'channel', 'channel voice-clone',
    ],
    'root': [ 'All' ],
	# 'root': [
    #     'member', 'member welcome', 'member make-webhook'
    #     'channel', 'channel hide', 'channel lock', 'channel voice-delete',
    #     'info', 'info channel',
    #     'thread', 'thread archive', 'thread delete',
    #     'message', 'message member', 'message channel', 'message edit',
    #     'message reply', 'message remove', 'message reactions',
    #     'reaction', 'reaction toggle-roles', 'reaction toggle',
    #     'role', 'role has', 'role update-position', 'role fetch',
    #     'event', 'event delete', 'event update-status', 'event fetch', 'event update',
    #     'teacode', 'teacode activity', 'teacode commands',
    # ],
}

dontSendEphemeralMsg = ['guide tag-rule']