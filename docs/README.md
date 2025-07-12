# Project Documentation

This `docs/` directory contains technical documentation for the Keydrop Bot project.
All modules and functions are summarized in the `functions/` subfolder.
Please consult these files prior to modifying the code base so that
existing business rules are not violated.

Additional documentation is available for the premium feature implementation in
`functions/premium.md`.
Documentation for the Discord OAuth integration can be found in
`functions/discord_oauth.md`.

The CI pipeline also provisions a **staging sandbox** whenever changes are merged
into `main`. This sandbox builds a container named `staging_bot`, runs the bot in
debug mode for three minutes and checks the logs for critical failures.
