# discord_oauth.py

Helper functions to authenticate users via Discord OAuth2 and manage
server membership.

## Functions
- `oauth_login() -> Dict[str, str]`
  Launch a browser-based OAuth flow and return the access token along with
  user details (`id`, `username`, `email`).
- `add_vip_role(user_id: str, access_token: str) -> None`
  Using the provided user token, join the configured guild and assign the
  VIP role using the bot token.
