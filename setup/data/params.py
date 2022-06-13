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

emojis = {
	'userjoin': '<:userjoin:902613054544560149>',
	'userleft': '<:userleft:902612227662684170>'
}

voice_data = {
	796115044374413332: { #voice-channels
		'vc-text':			795629763363864606,
		'vc-role':		867871623025262602,
	},
	867877610134700062: { #help-voice
		'vc-text':			802892768011223045,
		'vc-role':		818265370665943072,
	},
	909513881842515990: { #study-group
		'vc-text':			909572107271278673,
	},
	810187882153115648: { #committee corner
		'vc-text':			951593615191326860,
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
	'796732247470112769': { #polls
		'982778577877614643': {
			'🇾': 'Learn Blender'
		},
		'938141030673428550': {
			'🟤': 'Play Chess',
			'🟡': 'Coding Challenges'
		},
		'952311197594701895': {
			'🇾': 'Q/A Session'
		},
		'942529169223462923': {
			'🇾': 'Learn French'
		},
		'929867978969845770': {
			'🇾': 'Learn German'
		}
	},
	'783813544520712213': { #rules channel
		'881792967386480690': {
			'<:teacode_icon_dark:972803589145776189>': '🌱│Members',
			'<:teacode_icon_white:972803591452622858>': '🌱│Members',
		},
	},
	'802521765586010132': { #get-roles channel
		'904481592532164658': {
			'⚽': 'Html / Css',
			'🏀': 'Less',
			'🏈': 'Sass',
			'⚾': 'Tailwind Css',
			'🎾': 'Bootstrap',
			'🏐': 'Javascript',
			'🏉': 'Typescript',
			'🎱': 'jQuery',
			'🏓': 'Angular',
			'🏸': 'VueJs',
			'⛳': 'ReactJs',
			'🥋': 'EmberJs',
			'🥊': 'Svelte',
			'🏑': 'JSON',
			'🥌': 'XML',
			'🥏': 'YAML',
			'🪂': 'Nest JS',
			'⛸': 'Next JS',
			'🥅': 'Nuxt JS',
			'🛹': 'Gatsby',
		},
		'904484461826154546': {
			'🪛': 'Git',
			'🔧': 'Github',
			'🔨': 'GitLab',
			'🗡️': 'Bitbucket',
			'⛏️': 'Git Kraken',
			'🔩': 'Phabricator',
			'🪓': 'SourceTree',
			'🪚': 'Svn',
		},
		'904486579677052948': {
			'🚲': 'Docker',
			'🛵': 'Kubernetes',
			'🏍️': 'Jenkins',
			'🛺': 'Ansible',
			'🚗': 'SonarQube',
			'🚄': 'Selenium',
			'🚛': 'Gradle',
		},
		'904488442254225428': {
			'🪟': 'Windows',
			'🐧': 'Linux',
			'🌪️': 'Mac',
			'☄️': 'Windows Terminal',
			'🔥': 'Cmder',
			'🌊': 'Bash',
			'🌤️': 'iTerm2',
			'🌀': 'AWS - Amazon Web Services',
			'⚡': 'Microsoft Azure',
			'💧': 'Google Cloud',
			'☂️': 'Alibaba Cloud',
			'❄️': 'IBM Cloud',
			'🌙': 'Oracle Cloud',
			'☀️': 'Salesforce',
			'☁️': 'SAP',
		},
		'904490216847458365': {
			'🐇': 'NodeJs',
			'🐅': 'ExpressJs',
			'🐘': 'Php',
			'🐞': 'Laravel',
			'🦆': 'Symfony',
			'🐦': 'CodeIgniter',
			'🦈': 'C#',
			'🐟': 'VB.Net',
			'🐬': 'DotNet',
			'🦕': 'Java',
			'🦖': 'Spring / Spring Boot',
			'🐍': 'Python',
			'🦎': 'Django',
			'🐉': 'Flask',
			'🐢': 'Ruby',
			'🐌': 'Ruby on Rails',
			'🦅': 'Swift',
			'🐁': 'Go Lang',
			'⚙': 'Rust',
		},
		'904492639393566780': {
			'🏚': 'SQL',
			'🏘': 'NoSQL',
			'🏪': 'PL / SQL',
			'🏣': 'Transact-SQL',
			'⛩': 'GraphQL',
			'🏰': 'MySQL',
			'🗼': 'PostgreSQL',
			'🏭': 'SQLite',
			'🏟': 'SQL Server',
			'🏤': 'Oracle',
			'🏢': 'MongoDB',
			'🛖': 'Redis',
			'⛺': 'Firebase',
			'🏦': 'Cassandra',
			'🏯': 'RethinkDB',
			'🏛': 'Neo4j',
		},
		'904495036916449362': {
			'🇽': 'Xamarin Forms',
			'🇳': 'Xamarin Native',
			'🇰': 'Kotlin',
			'🇷': 'React Native',
			'🇩': 'Dart',
			'🇫': 'Flutter',
			'🇨': 'Ionic',
			'🇦': 'Android',
			'🇮': 'iOS',
		},
		'904499785426432001': {
			'📷': 'Adobe Photoshop',
			'⌨️': 'Adobe Illustrator',
			'📹': 'Adobe After Effects',
			'⏲️': 'Adobe Lightroom',
			'🎚️': 'Adobe XD',
			'📟': 'Adobe InDesign',
			'📼': 'Adobe Premiere Pro',
			'⌚': 'Autodesk Maya',
			'🕹️': 'Autodesk 3ds Max',
			'📺': 'Blender',
			'🎮': 'Adobe Fuse CC',
			'🎙️': 'Cinema 4D',
			'📻': 'Sketch',
			'☎️': 'SketchUp',
			'🖲️': 'Figma',
		},
		'904502258375479386': {
			'🍃': 'IntelliJ IDEA',
			'🍂': 'WebStorm',
			'🍏': 'PhpStorm',
			'🍎': 'PyCharm',
			'🌹': 'Rider (.Net)',
			'🍑': 'RubyMine',
			'🍒': 'DataGrip',
			'🍀': 'Android Studio',
			'🌺': 'Visual Studio',
			'🌷': 'VSCode',
			'🌱': 'Atom',
			'🍓': 'Sublime Text',
			'🌻': 'Brackets',
			'🌾': 'Eclipse',
			'🥑': 'NetBeans',
			'🌼': 'CodeBlocks',
			'💐': 'Vim',
			'🍇': 'Notepad++',
		},
		'904504466852700160': {
			'👾': 'C#',
			'🤖': 'C++',
			'💀': 'Unity',
			'🦔': 'Assembly',
			'🦝': 'C Language',
		},
		'904507027403980862': {
			'🍊': 'Technical Referent',
			'🥭': 'Technical Lead',
			'🥝': 'Database Administrator',
			'🥥': 'Programmer',
			'🍋': 'Developer',
			'🍇': 'Software Engineer',
			'🍐': 'Web Developer',
			'🍓': 'Web Designer',
			'🍈': 'FullStack Developer',
			'🥑': 'Frontend Developer',
			'🍅': 'Backend Developer',
			'🫐': 'Mobile Developer',
			'🍍': 'Game Developer',
			'🍎': 'Software Developer',
		},
		'904512821285503036': {
			'🖊️': 'Data Scientist',
			'✒️': 'Data Architect',
			'🖌️': 'Data Analyst',
			'✏️': 'Cloud Architect',
			'🖍️': 'Cloud Developer',
			'📏': 'Data Engineer',
			'🖋️': 'Cloud Engineer',
			'⛵': 'DevOps / DevSecOps',
			'🚢': 'DevOps Engineer',
			'🚀': 'DevOps Evangelist',
			'✈️': 'DevOps Software Developer',
			'🧪': 'Software Tester',
			'🌡':	'Quality Assurance',
		},
		'904515671080198164': {
			'🌁': 'Designer',
			'💾': 'Graphic Designer',
			'📷': 'UI Designer',
			'🖲️': 'UX Designer',
			'📽️': 'Film Maker / VFX',
			'🦬': 'Systems Administrator',
			'🐴': 'Network Administrator',
			'🦉': 'Network Engineer',
			'🐻‍❄️': 'Network Architect',
			'🦣': 'IT Security Engineer',
			'🦅': 'Security Specialist',
			'🐪': 'Security Systems Administrator',
			'🐿️': 'Security Engineer',
		},
		'904518697383759903': {
			'🥗': 'Artificial Intelligence',
			'🍕': 'Machine Learning',
			'🥟': 'DevOps / DevSecOps',
			'🍛': 'Blockchain',
			'🍩': 'VR / AR',
			'🧇': 'Cyber Security',
			'🧆': 'Cloud',
			'🥮': 'Big Data',
			'🎂': 'Internet Of Things',
			'🧀': 'Robotics / Electronics',
			'🍲': 'E-Commerce',
			'🍪': 'Developpement',
			'🍙': 'Game Developement',
			'🌰': 'Mobile Developement',
			'🍚': 'Data Science',
			'🍘': 'Computer Sciences',
			'🍨': 'Start-Ups / Entrepreneurship',
			'🥧': 'Project Management (Agile/Scrum)',
			'🥘': 'Business Intelligence',
			'🍿': 'Web 3.0',
		},
		'930480136166469683': {
			'☕': 'Hangout',
			'💭': 'Communication',
			'🎥': 'Workshops',
			'💻': 'Coding Challenges',
			'📱': 'Mock Interview',
		},
	},
}