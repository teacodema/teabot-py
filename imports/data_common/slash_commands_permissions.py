slash_commands_permissions = {
    'members': [
        'server info', 'role info', 'member info',
        'fun janken',
        'message tag-rule',
        'play', 'replay', 'pause', 'resume', 'previous', 'next', 'stop',
        'track', 'queue', 'clear-queue', 'refresh', 'leave',
    ],
    'hosts': [
        'member pick-speaker',
    ],
    'staff': [
        'message purge',
        'member pick-speaker', 'message poll',
        'member check-new-members', 'member update-new-members',
        'member toggle-role', 'member toggle-roles-members',
        'event subscribers', 'event create',
        'channel voice-clone',
    ],
	'root': [
        'member welcome',
        'channel hide', 'channel lock', 'channel voice-delete', 'channel channel-info',
        'thread archive', 'thread delete',
        'fun make-webhook', 'message member', 'message channel', 'message edit',
        'message reply', 'message remove',
        'reaction bot-reacts', 'reaction update-roles-reactions', 'reaction get-msg-reactions',
        'member has-role', 'role update-position', 'role fetch',
        'event delete', 'event edit-status', 'event fetch',
        'teabot activity', 'teabot list-commands',
    ],
}

dontSendEphemeralMsg = ['tag-rule']