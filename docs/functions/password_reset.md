# password_reset.py
Utilities for sending reset emails and updating passwords.

Credentials for the SMTP server are loaded from environment variables defined
in a `.env` file or from `config.json` if the variables are missing. The file
should contain:

```
SMTP_USER, SMTP_PASS, SMTP_HOST, SMTP_PORT
```

Functions: `request_reset`, `verify_token`, `reset_password`
