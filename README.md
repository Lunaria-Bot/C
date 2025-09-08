# Discord Bot (Minimal Railway Version)

## 🚀 Features
- Minimal bot setup for Discord
- `/ping` command to test if the bot is running

## 📦 Local Setup
1. Clone repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` (local only):
   ```env
   TOKEN=your_token
   GUILD_ID=your_guild_id
   ```
4. Run:
   ```bash
   python bot.py
   ```

## 🚀 Deployment on Railway
1. Push repo to GitHub
2. Create Railway project, link GitHub
3. Add environment variables in Railway:
   - `TOKEN` = your Discord bot token
   - `GUILD_ID` = your server ID
4. Deploy 🚀
