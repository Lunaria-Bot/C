# Discord Bot (Clean Railway, Renamed Env Vars)

This repo is intentionally minimal and avoids the variable name `TOKEN` during build.

## Env vars to set on Railway (Service → Variables)
- `DISCORD_TOKEN` = your Discord bot token
- `DISCORD_GUILD_ID` = your server ID

## Files
- `bot.py` — minimal bot with `/ping`
- `Procfile` — `worker: python -u bot.py`
- `requirements.txt` — `discord.py` only

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
