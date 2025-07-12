# cloud/permissions.py

Utility functions for fetching and validating user permissions stored in Firebase.

## Functions
- `fetch_permissions(user_id: str) -> Dict[str, Any]`
  Retrieve the permission document for the given user ID.
- `update_permissions(user_id: str, data: Dict[str, Any]) -> None`
  Update or create the user's permission data.
- `subscription_active(perms: Dict[str, Any]) -> bool`
  Return ``True`` if the expiration date is valid and in the future.
- `has_premium_access(perms: Dict[str, Any]) -> bool`
  Convenience helper to check premium access.
- `has_telegram_access(perms: Dict[str, Any]) -> bool`
  Convenience helper to check Telegram access.
