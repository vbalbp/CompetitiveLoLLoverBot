import datetime

import requests

from settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

def get_title(oauth_tokenfile=None):
    main_stream = {}
    expiration_date = None

    if oauth_tokenfile is not None:
        # TODO: Handle token file
        pass
    else:
        oauth_token = None
    
    # Request a new OAuth token if previous token expired or we have no token
    if expiration_date is None or datetime.datetime.now() >= expiration_date:
        response = requests.post(
            'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'.format(
                TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
            )
        )
        
        if response.status_code == 200:
            auth_response = response.json()

            expiration_date = (
                datetime.datetime.now()
                + datetime.timedelta(0, auth_response['expires_in'])
            )

            oauth_token = auth_response['access_token']

            # TODO: Store new token in tokenfile
        else:
            # TODO: Handle error code when requesting token
            pass

    # We have a token, go ahead with request
    response = requests.get(
        'https://api.twitch.tv/helix/search/channels?query=riotgames',
        headers={
            'client-id': TWITCH_CLIENT_ID,
            'Authorization': 'Bearer {}'.format(oauth_token)
        }
    )

    if response.status_code == 200:
        riot_response = response.json()
        
        main_stream = [
            stream
            for stream in riot_response['data']
            if stream['display_name'] == 'riotgames' and stream['is_live']
        ]
        main_stream = {} if not main_stream else main_stream[0]
    else:
        # TODO: Handle error code when requesting streams
        pass

    return main_stream.get('title', 'Worlds stream offline')
