from imports.data_server.channels_categories import *
from imports.data_server.members_roles import *

rules = [
    {
        "key": "1 - Guidelines & Terms",
        "value": f"Check here <#{textChannels['rules']}> + these links: Discord Community Guidelines (<https://discord.com/guidelines>) and Terms (<https://discord.com/terms>)",
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
        "value": f"If you have any ideas (for events, activities, rules .... ), Or you want to report a bug, or anything related to **TeaCode** (discord, website, social links),  you can post it here <#{textChannels['ask-staff']}>",
    },
    {
        "key": "6 - Contribute | Report",
        "value": f"If you see something against the rules or something that makes you feel unsafe, let the @Staff know. We want this server to be a welcoming space!",
    },
    {
        "key": "7 - Help Guide | Full",
        "value": f"Check for the Help Guide here <#{textChannels['read-me']}>",
    },
    {
        "key": "7 - Help Guide | How to Help",
        "value": f"""1- If someone contacts you by private message, tell them to post their question inside the group to get a faster answer and everyone can benefit.
2- If you want to share code, share it directly (check <https://teacode.ma/how-to-post-code> to know how), don't upload a file. If the code is too long or there are too many files, give us a link to a GitHub/GitLab/Bitbucket repository or Github Gists (<https://gist.github.com/>), Hastebin (<https://www.toptal.com/developers/hastebin>) ...
3- Get connected to the `🔉・Help Corner - Voice` to get this role <@&{roles['help-room']}> which allows you to invite others and see the `🧹・help-chat` channel 
4- When there is more than one helper helping the same person, respect each other and **DO NOT** try to show that you're more skilled or better than the others, the main goal is to help the person asking to achieve the solution on his own, not competing against each other.
5- Do Not Ask for help in exchange for money or Ask for money in exchange for help, otherwise post in <#{textChannels['jobs-internship']}>.
6- If you help someone, try to guide the person asking for help, providing the final solution is prohibited.""",
    },
    {
        "key": "7 - Help Guide | How to Ask for Help",
        "value": f"""1- Do not contact members by private message, the questions you have and the answers given can benefit everyone and you will be more likely to have a quick answer.
2- If you have a problem or question, make sure to do a minimum of research before. This server is dedicated to mutual aid, but our role is not to do Google searches for you!
3- Do not ask for solutions.
4- Ask for help in the `💡・Help Corner - Text` category and no where else. (*Otherwise the question will be deleted*)
5- When you ask a question in the `💡・Help Corner - Text`, include as many things as possible so that we can help you :
	- Explain the error message (or lack of errors!) You get.
	- Put a screenshot of the problem.
	- Tell us your code or the problematic lines.
6- If you want to share code, share it directly (check <https://teacode.ma/how-to-post-code> to know how), don't upload a file. If the code is too long or there are too many files, give us a link to a GitHub/GitLab/Bitbucket repository or Github Gists (<https://gist.github.com/>), Hastebin (<https://www.toptal.com/developers/hastebin>) ...
7- Members who can/want to help regularly visit the Help rooms, so when you ask for help, **DO NOT mention someone or everyone** , instead 👉 mention the role tags (ex: in <#{textChannels['python']}> use `@Python` `@Django` ..... , in <#{textChannels['js']}> use `@NodeJs` `@ReactJs` .... etc).
8- Do Not Post the same question in multiple channels.
9- Get connected to the `🔉・Help Corner - Voice` to get this role <@&{roles['help-room']}> which allows you to invite others and see the `🧹・help-chat` channel.
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
        "value": f"No spam or self-promotion (server invites, advertisements, etc) without permission from a @Staff. This includes DMing fellow members",
    },
    {
        "key": "10 - No NSFW",
        "value": "No NSFW or obscene content. This includes text, images, or links featuring nudity, sex, hard violence, or other graphically disturbing content"
    },
]
