import discord
import os
from dotenv import load_dotenv
from commands import backup, load

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
owner_id = int(os.getenv('OWNER_ID'))  # ID utilisateur de l'owner spécifié dans .env
prefix_value = os.getenv('DISCORD_PREFIX', '+')  # Défini dans le fichier .env

client = discord.Client()

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if not message.content.startswith(prefix_value):
        return  # Ignorer les messages qui ne commencent pas par le préfixe ou qui sont envoyés par le bot lui-même

    # Séparer le contenu du message pour distinguer la commande des arguments
    parts = message.content[len(prefix_value):].strip().split()
    if not parts:  # Vérifier s'il y a des commandes après le préfixe
        return  # Sortir si aucune commande n'est fournie après le préfixe

    command = parts[0].lower()  # La commande est le premier élément de parts
    args = parts[1:]  # Le reste sont des arguments

    if message.author.id != owner_id:
        return  # Seul le propriétaire peut exécuter les commandes

    try:
        await message.delete()  # Essayer de supprimer le message de commande

        # Exécuter les commandes en fonction du texte de la commande
        if command == 'backup':
            await backup.backup(message)
        elif command == 'load':
            await load.load(message, args)
        # Ajouter plus de commandes selon les besoins
    except Exception as e:
        print(f"Erreur lors du traitement de la commande {command}: {e}")


client.run(token)
