# password_reset.py
Utilities for sending reset e‑mails and updating passwords.

Credentials for the SMTP server are loaded from environment variables defined in
a `.env` file or from `config.json` if the variables are missing. The file
should contain the following keys:

```
SMTP_USER, SMTP_PASS, SMTP_HOST, SMTP_PORT
```

Tokens are generated using `secrets.token_urlsafe`, stored hashed with SHA256
and expire after one hour.

Functions available: `request_reset`, `verify_token`, `reset_password`
