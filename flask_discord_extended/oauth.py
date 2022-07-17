import requests
from requests_oauthlib import OAuth2Session
from flask import redirect, request
from .configs import *

class Oauth:

    def __init__(self, flask_discord):
        self.client_id = flask_discord.app.config["DISCORD_CLIENT_ID"]
        self.client_secret = flask_discord.app.config["DISCORD_CLIENT_SECRET"]
        self.redirect_uri = flask_discord.app.config["DISCORD_OAUTH_REDIRECT_URI"]
        self.scope = flask_discord.app.config["DISCORD_OAUTH_SCOPE"]
        self.discord_login_url = self._make_login_url()
        self.discord_token_url = DISCORD_TOKEN_URL
        self.discord_api_url = DISCORD_API_BASE_URL


    def _make_login_session(self):
        return OAuth2Session( 
        client_id = self.client_id,
        scope = self.scope,
        redirect_uri = self.redirect_uri
        )


    def _make_login_url(self):
        return self._make_login_session().authorization_url(DISCORD_AUTHORIZATION_BASE_URL)[0]


    def get_login_url(self):
        return self.discord_login_url


    def redirect_login(self):
        return redirect(self.discord_login_url)


    def _get_access_token(self):
        auth = self._make_login_session().fetch_token(
                self.discord_token_url,
                client_secret = self.client_secret,
                authorization_response = request.url
            )
        return auth["access_token"]


    def _get_user_json(self, access_token):
        url = f"{self.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}
 
        user_object = requests.get(url = url, headers = headers).json()
        return user_object


    def callback(self):
        access = self._get_access_token()

        return self._get_user_json(access)