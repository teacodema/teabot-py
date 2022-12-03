from imports.data.properties import *


player_params = {
	'current_played': None,
}

appParams = {
	'every_n_weeks_min': 1,
	'every_n_weeks_max': 4,
	'recurrence_min': 2,
	'recurrence_max': 5,
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

voice_roles = {
	900514598057287740: 930832493312102440, #talk|event
	899100431454699520: 930832498781466674,	#communication
	1048375097339158609: 930832498781466674, #communication - stage
	899100694148157530: 930833564315045898, #workshops
	899099886195212339: 930833844490362961, #coding-challenges
	899100166500528138: 930833853097066526, #mock-interview
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
        "key": "5 - No Cheating",
        "value": "Cheating in school related stuff (exams, projects .. etc) is prohibited",
    },
    {
        "key": "6 - Contribute | Suggestions",
        "value": f"If you have any ideas (for events, activities, rules .... ), Or you want to report a bug, or anything related to **TeaCode** (discord, website, social links),  you can post it here <#{textChannels['suggestions']}>",
    },
    {
        "key": "6 - Contribute | Report",
        "value": f"If you see something against the rules or something that makes you feel unsafe, let the <@&{roles['staff']}> know. We want this server to be a welcoming space!",
    },
    {
        "key": "7 - Help Guide | Full",
        "value": f"Check for the Help Guide here <#{textChannels['read-me']}>",
    },
    {
        "key": "7 - Help Guide | How to Help",
        "value": f"""1- If someone contacts you by private message, tell them to post their question inside the group to get a faster answer and everyone can benefit.
2- If you want to share code, share it directly (check <https://teacode.ma/how-to-post-code> to know how), don't upload a file. If the code is too long or there are too many files, give us a link to a GitHub/GitLab/Bitbucket repository or Github Gists (<https://gist.github.com/>), Hastebin (<https://www.toptal.com/developers/hastebin>) ...
3- Get connected to the **__<#{categories['help-voice']}>__** to get this role <@&{roles['help-room']}> which allows you to invite others and see the **__<#{textChannels['help-chat']}>__** channel 
4- When there is more than one helper helping the same person, respect each other and DO NOT try to show that you're more skilled or better than the others, the main goal is to help the person asking to achieve the solution on his own, not competing against each other.
5- Do Not Ask for help in exchange for money or Ask for money in exchange for help, otherwise post in <#{textChannels['jobs-internship']}>.
6- If you help someone, try to guide the person asking for help, providing the final solution is prohibited.""",
    },
    {
        "key": "7 - Help Guide | How to Ask for Help",
        "value": f"""1- Do not contact members by private message, the questions you have and the answers given can benefit everyone and you will be more likely to have a quick answer.
2- If you have a problem or question, make sure to do a minimum of research before. This server is dedicated to mutual aid, but our role is not to do Google searches for you!
3- Do not ask for solutions.
4- Ask for help in the **__<#{categories['help-text']}>__** category and no where else. (*Otherwise the question will be deleted*)
5- When you ask a question in the **__<#{categories['help-text']}>__**, include as many things as possible so that we can help you :
	- Explain the error message (or lack of errors!) You get.
	- Put a screenshot of the problem.
	- Tell us your code or the problematic lines.
6- If you want to share code, share it directly (check <https://teacode.ma/how-to-post-code> to know how), don't upload a file. If the code is too long or there are too many files, give us a link to a GitHub/GitLab/Bitbucket repository or Github Gists (<https://gist.github.com/>), Hastebin (<https://www.toptal.com/developers/hastebin>) ...
7- Members who can/want to help regularly visit the Help rooms, so when you ask for help, **DO NOT mention someone or everyone** , instead 👉 mention the role tags (ex: in <#{textChannels['python']}> use <@&{roles['python']}> <@&{roles['django']}> ..... , in <#{textChannels['js']}> use <@&{roles['nodejs']}> <@&{roles['reactjs']}> .... etc).
8- Do Not Post the same question in multiple channels.
9- Get connected to the **__<#{categories['help-voice']}>__** to get this role <@&{roles['help-room']}> which allows you to invite others and see the **__<#{textChannels['help-chat']}>__** channel.
10- Do Not Ask for help in exchange for money or Ask for money in exchange for help, otherwise post in <#{textChannels['jobs-internship']}>.
11- Before asking your question visit these websites <https://dontasktoask.com/>, <https://xyproblem.info/>, <https://nohello.net/>.""",
    },
	{
		"key": "7 - Help Guide | How to post code",
		"value": """You can post a block of code and enable syntax highlighting using 3 back quotes followed by the language name, for example for Python (copy this code :point_down: and change py to css, js, .... etc): 
\`\`\`py
  // python code
\`\`\`
or 
\`\`\`css
  // css code
\`\`\`

You can find more informations on message formatting here :
<https://support.discord.com/hc/en-us/articles/210298617-Bases-de-la-mise-en-forme-de-texte-Markdown-mise-en-forme-du-chat-gras-italique-soulign%C3%A9->
see image below also :point_down:
https://teacode.ma/assets/shared/img/extra/markdown_code.gif
"""
	},
	{
		"key": "7 - Help Guide | Share Code",
		"value": """If you want to share code, share it directly (check <https://teacode.ma/how-to-post-code> to know how), don't upload a file. If the code is too long or there are too many files, give us a link to a GitHub/GitLab/Bitbucket repository or Github Gists (<https://gist.github.com/>), Hastebin (<https://www.toptal.com/developers/hastebin>) ..."""
	},
	{
		"key": "7 - Help Guide | No Money asked",
		"value": f"""Do Not Ask for help in exchange for money or Ask for money in exchange for help, otherwise post in <#{textChannels['jobs-internship']}>."""
	},
	{
		"key": "7 - Help Guide | Before Asking for help",
		"value": """Before asking your question visit these websites <https://dontasktoask.com/>, <https://xyproblem.info/>, <https://nohello.net/>."""
	},
    {
        "key": "8 - Server Guide",
        "value": f"Check for FAQ (Frequently Asked Questions) here <#{textChannels['faqs']}>",
    },
    {
        "key": "9 - No Spam / Promo",
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
			'🍪': 'Development',
			'🍙': 'Game Development',
			'🌰': 'Mobile Development',
			'🍚': 'Data Science',
			'🍘': 'Computer Sciences',
			'🍨': 'Start-Ups / Entrepreneurship',
			'🥧': 'Project Management (Agile/Scrum)',
			'🥘': 'Business Intelligence',
			'🍿': 'Web 3.0',
		},
		'930480136166469683': {
			'☕': 'Talk┊Event',
			'💭': 'Communication',
			'🎥': 'Workshops',
			'💻': 'Coding Challenges',
			'📱': 'Mock Interview',
		},
		'969927727580868628': {
			'🎓': 'Student',
			'💼': 'Employee',
			'🎒': 'Freelancer',
			'👔': 'Entrepreneur',
		},
	},
}