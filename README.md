# Flask-Discord-Extended

The Python OAuth2 and Discord Bot Commands for Flask applications.

### Installation

To install current latest release you can use following command:

```sh
python3 -m pip install Flask-Discord-Extended
```

### Code Example

```python
from flask_discord_extended import FlaskDiscord
from flask import Flask

import os

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"


app.config["DISCORD_CLIENT_ID"] = ""                # Discord Client Id
app.config["DISCORD_CLIENT_SECRET"] = ""            # Discord Client Secret
app.config["DISCORD_OAUTH"] = True                  # Set True if you need Oauth feature
app.config["DISCORD_OAUTH_SCOPE"] = ['identify']    # Scopes for Oauth
app.config["DISCORD_OAUTH_REDIRECT_URI"] = ""       # Redirect Uri for Oauth
app.config["DISCORD_AUTHORIZATION"] = ""            # Bot aothorization token

Discord = FlaskDiscord(app)

@app.route('/')
def index():
    return """
    <form action = "/discord-login" method = "GET">
        <button type = "submit" style = "padding: 15px; background:rgb(88, 101, 242); cursor: pointer; color: white; border: 0px; border-radius:5px">LogIn With Discord</button>
    <form>
    """


@app.route('/discord-login')
def login():
    # Redirects to Discord login
    return Discord.Oauth.redirect_login()


@app.route('/callback')
def test():
    user = Discord.Oauth.callback()

    """
        Each function from the Utilities returns an json response object

        The bot whose authorization code is set to the app needs to be in the same server
        with the user
    """
    Discord.Utilities.add_role(guild="GUILD_ID", user_id=user["id"], role="ROLE_ID")
    Discord.Utilities.remove_role(guild="GUILD_ID", user_id=user["id"], role="997877802265235586")
    Discord.Utilities.get_guild_member_data(guild="GUILD_ID", user_id=user["id"])
    Discord.Utilities.set_nickname(guild="GUILD_ID", user_id=user["id"], nickname="Any nickname")

    Discord.Utilities.send_dm(user_id=user["id"], content="Content")
    return user


if __name__ == "__main__":
    app.run(debug=True)
```

### Requirements

- Flask
- requests_oauthlib
