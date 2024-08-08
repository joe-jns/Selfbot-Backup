@echo off
echo Création du fichier .env...

echo DISCORD_TOKEN= > .env
echo OWNER_ID= >> .env
echo DISCORD_PREFIX=+ >> .env

echo Installation des dépendances...
pip install -r requirements.txt

echo Le fichier .env a été créé avec succès et les dépendances ont été installées.
pause
