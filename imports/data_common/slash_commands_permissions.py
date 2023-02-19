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
        'member check-new', 'member update-new',
        'member toggle-role', 'member toggle-roles',
        'event subscribers', 'event create',
        'channel voice-clone',
    ],
	'root': [
        'member welcome',
        'channel hide', 'channel lock', 'channel voice-delete', 'channel info',
        'thread archive', 'thread delete',
        'member make-webhook', 'message member', 'message channel', 'message edit',
        'message reply', 'message remove',
        'reaction bot-reacts', 'reaction update-roles-reactions', 'reaction get-msg-reactions',
        'member has-role', 'role update-position', 'role fetch',
        'event delete', 'event edit-status', 'event fetch',
        'teabot activity', 'teabot list-commands',
    ],
}

dontSendEphemeralMsg = ['guide tag-rule']