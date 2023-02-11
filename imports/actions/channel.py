
async def toggle_lock_channel(channel, role, value):
    await channel.set_permissions(role, view_channel=True,
                                        send_messages=value,
                                        create_public_threads=value,
                                        create_private_threads=value,
                                        send_messages_in_threads=value,
                                        connect=value,
                                        speak=True,
                                        use_voice_activation=True
                                        )

async def toggle_hide_channel(channel, role, value):
    await channel.set_permissions(role, view_channel=value,
                                        send_messages=True,
                                        create_public_threads=True,
                                        create_private_threads=True,
                                        send_messages_in_threads=True,
                                        connect=True,
                                        speak=True,
                                        use_voice_activation=True
                                        )