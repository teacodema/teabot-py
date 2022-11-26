
async def toggle_lock_channel(channel, role, value):
    await channel.set_permissions(role, view_channel=True, send_messages=value,
                                        connect=value, create_public_threads=value,
                                        create_private_threads=value,
                                        send_messages_in_threads=value)

async def toggle_hide_channel(channel, role, value):
    await channel.set_permissions(role, view_channel=value)