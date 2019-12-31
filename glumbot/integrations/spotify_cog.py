import spotipy
import spotipy.util as util
from pathlib import Path
from twitchio.ext import commands as commands

class SpotifyCog:
    _AUTH_SCOPE = 'user-read-playback-state'

    def __init__(self, bot):
        self.bot = bot
        bot.spotify_cog = self

        # Authenticate...
        username = bot.config['SPOTIFY_USERNAME']
        cache_path = str((Path(bot.config['INSTANCE_PATH']) / bot.config['SPOTIFY_AUTH_CACHE_FILENAME']).resolve().absolute())
        token = util.prompt_for_user_token(username, SpotifyCog._AUTH_SCOPE, 
            client_id=bot.config['SPOTIFY_CLIENT_ID'],
            client_secret=bot.config['SPOTIFY_CLIENT_SECRET'],
            redirect_uri=bot.config['SPOTIFY_REDIRECT_URI'],
            cache_path=cache_path
        )

        if token:
            self.client = spotipy.Spotify(auth=token)
            bot.logger.info('Spotify - successfully authenticated!')
        else:
            self.client = None
            bot.logger.warn('Spotify - cannot authenticate user \'\'.'.format(username))