from setup.data.properties import *


player_params = {
	'current_played': None,
}

appParams = {
	'newMembershipPeriode': 7, # in days
	'inviteMaxAge': 604800, # in seconds <=> 1 week
	'inviteMaxUses': 10,
	'blue': 0x1da1f2,
	'notifyOffset': 15
}

voice_data = {
	977901284189425755: { #testing
		'vc-text':			978373773063499777,
	},
	982652617589129227: { #voice-channels
		'vc-text':			982653718346465340,
		'vc-role':		978372227441524816,
	},
	982653086755606568: { #help-voice
		'vc-text':			982653507029061693,
		'vc-role':		982653192003260476,
	}
}

rules = [
    {
        "key": "1 - Guidelines & Terms",
        "value": "Follow the Discord Community Guidelines (<https://discord.com/guidelines>) and Terms (<https://discord.com/terms>)",
    },
    {
        "key": "2 - Behavior",
        "value": "Be kind, Be respectful, Be considerate, Treat everyone with respect, think about how your contribution will affect others in the community, for more details read this <https://conversation.guide>",
    },
    {
        "key": "3 - Interaction",
        "value": "When you join any voice/text channel, please avoid saying/writing any obscene content (spam, NSFW, ..etc) or bad words (directly or indirectly), otherwise you risk getting kicked/banned from the server",
    },
    {
        "key": "4 - Profile",
        "value": "We keep the right to ask you to change your nickname/username/description if it's not readable or contains any bad words",
    },
    {
        "key": "5 - Cheating",
        "value": "Cheating in school related stuff (exams, projects .. etc) is prohibited",
    },
    {
        "key": "6 - Contribute",
        "value": f"If you see something against the rules or something that makes you feel unsafe, let the <@&{roles['staff']}> know. We want this server to be a welcoming space!",
    },
    {
        "key": "7 - Help Guide",
        "value": f"Check for the Help Guide here <#{textChannels['read-me']}>",
    },
    {
        "key": "8 - Server Guide",
        "value": f"Check for FAQ (Frequently Asked Questions) here <#{textChannels['faqs']}>",
    },
    {
        "key": "9 - No promo",
        "value": f"No spam or self-promotion (server invites, advertisements, etc) without permission from a <@&{roles['staff']}>. This includes DMing fellow members",
    },
    {
        "key": "10 - No NSFW",
        "value": "No NSFW or obscene content. This includes text, images, or links featuring nudity, sex, hard violence, or other graphically disturbing content"
    },
]

reactions = {
	'965359255966339083': { #polls
		'985826087206518794': {
			'🟤': 'Staff',
			'🟡': 'Member',
		}
	}
}