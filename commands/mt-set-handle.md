---
name: mt-set-handle
description: Verify your X identity and set your Twitter handle for this session
---

# mt-set-handle

Verify your X identity so all commands know who you are.

Your handle is derived from your verified session token — not from a string you type. This protects against anyone impersonating another trader.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable.
2. If `MT_AUTH_TOKEN` is set, call `trader_my_stats` with `auth_token` to resolve and confirm the verified handle.
3. Confirm: "Verified as @{handle}. All commands will use this identity."
4. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL. Tell the user to authenticate with X. Once they provide their token, persist it for future sessions using the platform-appropriate method, then set it in the current session and run `/mt-set-handle` again:
   - **macOS**: append `export MT_AUTH_TOKEN=<token>` to `~/.zshenv`
   - **Linux**: append `export MT_AUTH_TOKEN=<token>` to `~/.bashrc` (or `~/.profile` for login shells)
   - **Windows (PowerShell)**: run `[System.Environment]::SetEnvironmentVariable('MT_AUTH_TOKEN', '<token>', 'User')` to persist at user level; also set in current session with `$env:MT_AUTH_TOKEN='<token>'`

## Notes

- Identity is verified server-side via X OAuth 2.0 — it cannot be spoofed
- The session token expires in 30 days; run `/mt-set-handle` again after re-authenticating
- Commands that look up OTHER traders (e.g., `/mt-last <handle>`) still accept an explicit handle
