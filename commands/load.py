import os
import json
import discord


async def load(message, args):
    backup_folder = 'backups'
    backups = os.listdir(backup_folder)
    backups = [f for f in backups if f.endswith('.json')]

    if len(backups) == 0:
        return await message.channel.send("Aucune sauvegarde trouvée.")

    if not args:
        backup_list = "\n".join([f"{i + 1}. {backups[i]}" for i in range(len(backups))])
        confirmation_message = await message.channel.send(f"Voici les sauvegardes disponibles:\n{backup_list}\nVeuillez spécifier le numéro de la sauvegarde à charger.")
        return confirmation_message

    try:
        index = int(args[0]) - 1
        if index < 0 or index >= len(backups):
            return await message.channel.send("Index de sauvegarde invalide.")
    except ValueError:
        return await message.channel.send("Veuillez spécifier un numéro valide.")

    backup_file = os.path.join(backup_folder, backups[index])

    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    guild = message.guild

    # Supprimer les rôles et les salons existants
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except:
                pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # Restaurer les rôles
    roles = {}
    for role_data in data['roles']:
        role = await guild.create_role(
            name=role_data['name'],
            permissions=discord.Permissions(role_data['permissions']),
            colour=discord.Colour(role_data['color']),
            hoist=role_data['hoist'],
            mentionable=role_data['mentionable']
        )
        roles[role.name] = role

    # Restaurer les salons
    for channel_data in data['channels']:
        if channel_data['type'] == 'text':
            await guild.create_text_channel(
                name=channel_data['name'],
                category=discord.utils.get(guild.categories, name=channel_data['category'])
            )
        elif channel_data['type'] == 'voice':
            await guild.create_voice_channel(
                name=channel_data['name'],
                category=discord.utils.get(guild.categories, name=channel_data['category'])
            )
        elif channel_data['type'] == 'category':
            await guild.create_category(name=channel_data['name'])

    confirmation_message = await message.channel.send(f"Restauration de la sauvegarde {backup_file} terminée.")
    return confirmation_message
