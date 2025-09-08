# Discord Bot (Full Features)

This bot includes:
- `/ping` → test
- `/embed` → create custom embed (admins only)
- `/autorole <role>` → send button to toggle role
- `/setup <@role1,@role2,...>` → send multi-role selector

## Env vars to set on Railway (Service → Variables)
- `DISCORD_TOKEN` = your Discord bot token
- `DISCORD_GUILD_ID` = your server ID

## Persistence
Autorole and setup messages are saved in `storage.json` to survive restarts.

## Local run (optional)
Create a `.env` locally (do NOT commit it):
```
DISCORD_TOKEN=your_token_here
DISCORD_GUILD_ID=your_guild_id_here
```

Then run:
```
python bot.py
```
