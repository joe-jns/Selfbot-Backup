import os
import json
import discord

async def backup(message):
    server_name = message.guild.name
    server_id = message.guild.id
    backup_folder = 'backups'
    backup_file = f'{backup_folder}/{server_name.replace(" ", "_").replace("/", "_")}_{server_id}.json'

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    data = {
        'name': server_name,
        'id': server_id,
        'roles': [],
        'channels': []
    }

    # Sauvegarde des rôles
    for role in message.guild.roles:
        data['roles'].append({
            'name': role.name,
            'permissions': role.permissions.value,
            'position': role.position,
            'color': role.color.value,
            'hoist': role.hoist,
            'mentionable': role.mentionable
        })

    # Sauvegarde des salons
    for channel in message.guild.channels:
        channel_data = {
            'name': channel.name,
            'id': channel.id,
            'type': str(channel.type)
        }
        if isinstance(channel, discord.TextChannel):
            channel_data['topic'] = channel.topic
            channel_data['nsfw'] = channel.is_nsfw()
            channel_data['category'] = channel.category.name if channel.category else None
        elif isinstance(channel, discord.VoiceChannel):
            channel_data['bitrate'] = channel.bitrate
            channel_data['user_limit'] = channel.user_limit
            channel_data['category'] = channel.category.name if channel.category else None
        elif isinstance(channel, discord.CategoryChannel):
            channel_data['channels'] = [c.id for c in channel.channels]
        data['channels'].append(channel_data)

    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    confirmation_message = await message.channel.send(f'Backup de {server_name} terminée.')
    return confirmation_message
