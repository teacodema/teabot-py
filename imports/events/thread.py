
from imports.actions.message import *
from imports.actions.common import *

def init_events_thread(params):

    bot = params['bot']

    @bot.event
    async def on_raw_thread_delete(payload):
        try:
            thread = payload.thread
            log = bot.get_channel(textChannels['log-txt'])
            user_mention = await toggle_user_mention(bot, thread.owner, roles['viewer'])
            log_thread = await make_thread(log, f'🗑 Thread - {user_mention} in {toggle_channel_mention(thread.parent)}')

            msg = '──────────────────────'
            msg += f'\n🗑 by {user_mention} in {thread.parent.mention}'
            msg += f'\nAuthor ID : {thread.owner_id}'
            msg += f'\nThread : {thread.name}'
            created_at = getTimeUtcPlusOne(thread.created_at, "%d %B %Y - %H:%M")
            msg += f'\n📅 {created_at}'
            await log_thread.send(msg.strip())
            await log_thread.edit(archived=True)
        except Exception as ex:
            print('----- on_raw_thread_delete(evt) -----')
            print(ex)
            await log_exception(ex, 'on_raw_thread_delete(evt)', None, bot)
