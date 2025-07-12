# user_interface.py

Implements login, registration and profile screens using `customtkinter` and
Firebase for persistence.

## Functions
- `_load_pyrebase() -> pyrebase.pyrebase.Firebase`
  Load Firebase credentials from `firebase_config.json` and return a Pyrebase
  client instance.
- `_save_session(user: Dict[str, Any]) -> None`
  Persist authentication tokens to `user_session.json` so the user can remain
  logged in across sessions.
- `autenticar_usuario(email: str, senha: str) -> Dict[str, Any]`
  Authenticate the user via Firebase email/password.
- `registrar_usuario(email: str, senha: str) -> Dict[str, Any]`
  Create a new user account in Firebase authentication and save the session.
- `carregar_dados_usuario(user_id: str) -> Optional[Dict[str, Any]]`
  Retrieve stored profile information for the given user ID from Firebase.
- `sincronizar_perfil(user_id: str, nome: str, lucro_total: float, tempo_total_min: int, bots_ativos_max: int) -> None`
  Persist profile metrics and update ranking using functions from
  `cloud/firebase_client.py`.
- `discord_oauth_login() -> Dict[str, str]`
  Helper defined in `discord_oauth.py` used by `LoginFrame` to allow login via Discord.

Additional Tkinter `Frame` subclasses (`LoginFrame`, `RegisterFrame`,
`ProfileFrame`, `RankingFrame`, `StoreFrame`) implement the GUI components for
interacting with the bot. `StoreFrame` provides a simple shopping interface
allowing the user to add premium items to a cart and proceed with payment via
Pix. The professional desktop version under `bot_keydrop/gui/` exposes a
similar `StoreFrame` class for integration with the full-featured GUI.
