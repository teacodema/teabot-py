slash_commands_permissions = {
    'members': [
        'info server', 'info role', 'info member',
        'fun janken',
        'guide tag-rule',
        'audio play', 'audio replay', 'audio pause', 'audio resume', 'audio previous', 'audio next', 'audio stop',
        'audio track', 'audio queue', 'audio clear', 'audio refresh', 'audio leave',
    ],
    'hosts': [
        'member pick-speaker',
    ],
    'staff': [
        'message purge',
        'member pick-speaker', 'message poll',
        'role toggle', 'role toggle-multiple',
        'event subscribers', 'event create',
        'channel voice-clone',
    ],
	'root': [
        'member welcome',
        'channel hide', 'channel lock', 'channel voice-delete', 'info channel',
        'thread archive', 'thread delete',
        'member make-webhook', 'message member', 'message channel', 'message edit',
        'message reply', 'message remove',
        'reaction toggle-roles', 'message reactions',
        'role has', 'role update-position', 'role fetch',
        'event delete', 'event update-status', 'event fetch', 'event update',
        'teacode activity', 'teacode commands', 'reaction toggle'
    ],
}

dontSendEphemeralMsg = ['guide tag-rule']