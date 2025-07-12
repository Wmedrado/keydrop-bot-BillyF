# bot_keydrop.backend.premium

Utilities for handling premium products and permissions.

## Functions
- `purchase_product(user_id: str, product_id: str) -> None`
  Register the purchase of a premium product for the given user. Subscriptions update
  the permission flags and store an expiration date. Cosmetic items are stored in
  the `items_owned` list.

- `check_premium_validity(user_id: str) -> Dict`
  Validate the user's expiration date and revoke permissions if expired. Returns the
  current permission dictionary.

- `has_permission(user_id: str, permission: str) -> bool`
  Convenience helper that checks if a user currently has a specific permission.

The following cosmetic items are available for purchase and will be stored in
`items_owned`:

- `frame_neon` – contorno brilhante em tons neon
- `frame_diamond` – efeito cintilante semelhante a diamante
- `frame_gold` – borda dourada clássica
