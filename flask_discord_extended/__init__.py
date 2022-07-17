import warnings
from .oauth import Oauth
from .utilities import Utilities


class FlaskDiscord(object):

    def __init__(self, app = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        required_keys = ['DISCORD_CLIENT_ID', 'DISCORD_CLIENT_SECRET']

        oauth_keys = ['DISCORD_OAUTH_REDIRECT_URI', 'DISCORD_OAUTH_SCOPE']

        for key in required_keys:
            if key not in app.config:
                warnings.warn(f'{key} is not set.')

        if 'DISCORD_OAUTH' in app.config and app.config['DISCORD_OAUTH'] == True:
            for key in oauth_keys:
                if key not in app.config:
                    warnings.warn(f'{key} is not set.')
            self.Oauth = Oauth(self)

        self.Utilities = Utilities(self)

