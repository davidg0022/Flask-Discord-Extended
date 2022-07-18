import requests
import json
from .configs import DISCORD_API_BASE_URL

from . import exceptions

class Utilities():

    def __init__(self, flask_app):
        self.authorization = flask_app.app.config["DISCORD_AUTHORIZATION"]
        self.headers = self._make_headers(self.authorization)

    def _make_headers(self, authorization = ""):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "authorization" : f"Bot {authorization}"
        }
        return headers
    
    def _request(self, route, method, payload = None):
        route = DISCORD_API_BASE_URL + route
        if payload == None:
            response = requests.request(method, route, headers = self.headers)
        else:
            response = requests.request(method, route, data = json.dumps(payload), headers = self.headers)

        if response.status_code == 401:
            raise exceptions.Unauthorized()
        
        if response.status_code == 429:
            raise exceptions.RateLimited(response.json(), response.headers)

        return response.json()

    def send_chanel_message(self, content, chanel):
        payload = {
            "content": content,
            # "embeds":[{
            #     "title":"Test",
            #      'color':0x0099ff,
            #      'fields':[
            #         {"name":"Regular field title", "value":"test","inline":True},
            #         {"name":"Regular field title", "value":"test","inline":True},
            #         {"name":"Regular field title", "value":"test","inline":True},
            #         {"name":"Regular field title", "value":"test"},
            #         {"name":"Regular field title", "value":"test","inline":True},
            #         {"name":"Regular field title", "value":"test","inline":True},
            #         ],
            #         "image":{
            #             "url":"https://i.imgur.com/AfFp7pu.png"
            #         }
            #         "footer":{
                        
            #         }
            #      }]
        }
        return self._request(route = f"/channels/{chanel}/messages", method = "POST", payload = payload)


    def get_guild_member_data(self, guild, user_id):
        return self._request(route = f"/guilds/{guild}/members/{user_id}", method = "GET")
    

    def add_role(self, guild, user_id, role):
        try:
            roles = self.get_guild_member_data(guild, user_id)["roles"]
        except KeyError:
            return {}
        if role not in roles:
            roles.append(role)
        payload = {
            "roles": roles
        }
        return self._request(route = f"/guilds/{guild}/members/{user_id}", method = "PATCH", payload = payload)


    def remove_role(self, guild, user_id, role):
        try:
            roles = self.get_guild_member_data(guild, user_id)["roles"]
        except KeyError:
            return {}
        if role in roles:
            roles.remove(role)
        payload = {
            "roles": roles
        }
        return self._request(route = f"/guilds/{guild}/members/{user_id}", method = "PATCH", payload = payload)

    
    def set_nickname(self, guild, user_id, nickname):
        payload = {
            "nick":nickname
        }
        return self._request(route = f"/guilds/{guild}/members/{user_id}", method = "PATCH", payload = payload)
    
    def set_chanel_name(self, chanel, name):
        payload = {
            "name": name
        }
        return self._request(route = f"/channels/{chanel}", method = "PATCH", payload = payload)

    
    def send_dm(self, user_id, content):
        payload = {
            "recipients" : [user_id]
        }
        try:
            chanel = self._request(route = "/users/@me/channels", method = "POST", payload = payload)["id"]
        except KeyError:
            return {}
        return self.send_chanel_message(chanel = chanel, content = content )

    def get_profile_data(self, user_id):
        return self._request(route=f"/users/{user_id}", method="GET")
        
    def get_avatar_url(self, user_id):
        avatar_id = self.get_profile_data(user_id=user_id)["avatar"]
        return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}"