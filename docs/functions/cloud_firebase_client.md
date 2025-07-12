# cloud/firebase_client.py

This module provides helper functions to integrate with Firebase. It lazily
initializes the Firebase app and exposes utilities to persist user profiles,
update ranking data and upload profile images.

## Functions
- `initialize_firebase() -> firebase_admin.App`
  Initialize Firebase using credentials located at `../firebase_credentials.json`.
- `salvar_perfil(user_id: str, nome: str, lucro_total: float, tempo_total_min: int, bots_ativos_max: int) -> None`
  Store or update a user's profile in the realtime database and update the
  overall ranking.
- `atualizar_ranking(user_id: str, lucro_total: float) -> None`
  Update the global ranking node with the provided total profit.
- `upload_foto_perfil(user_id: str, caminho_imagem: str) -> str`
  Upload the given image file to Firebase Storage and associate the returned URL
  with the user profile.
- `registrar_compra(user_id: str, itens: List[Dict[str, Any]]) -> None`
  Persist information about a purchase attempt under `compras/{user_id}`.
