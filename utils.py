import os

def load_prefix():
    return os.getenv('DISCORD_PREFIX', '+')

def save_prefix(new_prefix):
    os.environ['DISCORD_PREFIX'] = new_prefix
    with open('.env', 'r') as file:
        lines = file.readlines()
    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith('DISCORD_PREFIX'):
                file.write(f"DISCORD_PREFIX={new_prefix}\n")
            else:
                file.write(line)
