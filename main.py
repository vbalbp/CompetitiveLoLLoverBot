import sys
import time

import yaml
import discord

from worlds_stream import get_title
from settings import DISCORD_TOKEN, CHANNEL_ID

with open('data/teams.yml', 'r') as hdl:
    TEAMS = yaml.safe_load(hdl)

def map_teams(title_string):
    team_dict = TEAMS.get('teams', {})

    for team_name, team_info in team_dict.items():
        title_string = title_string.replace(
            team_name,
            '{}{}'.format(
                team_info.get('abbr', team_name),
                ' ({})'.format(team_info['region'])
                if 'region' in team_info
                else ''
            )
        )

    return title_string

client = discord.Client()

@client.event
async def on_ready():
    # Get channel to edit
    for guild in client.guilds:
        channel = [channel for channel in guild.voice_channels if channel.id == CHANNEL_ID]

    # Edit channel with the right string
    if channel:
        title = get_title()
        title = map_teams(
            ' : '.join([
                half.strip()
                for half in title.split(':')[::-1]
            ])
        )
        await channel[0].edit(name=title)

    await client.close()

def main():
    client.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()
