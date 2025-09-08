# Discord Bot (Ping, Embed, Autorole, Say, Debug)

This bot includes:
- `/ping` → test
- `/embed` → create custom embed (admins only, with title, description, color, thumbnail, image)
- `/autorole <role>` → send button to toggle role
- `/say <message> [channel] [embed]` → make the bot send a normal or embed message
- `/debug` → show bot and server information (admins only, embed output)

## Env vars to set on Railway (Service → Variables)
- `DISCORD_TOKEN` = your Discord bot token
- `DISCORD_GUILD_ID` = your server ID

## Autorole setup
- Make sure "Server Members Intent" is enabled in the Discord Developer Portal.
- Ensure the bot's role is **higher** than the roles it should assign.

## Persistence
Autorole messages are saved in `storage.json` to survive restarts.

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
