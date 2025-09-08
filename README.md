# Discord Bot with Mazoku Reminder (Debug Version)

## Features
- /embed → Create custom embeds with colors, images, footer, etc.
- /say → Make the bot say something.
- /debug → Debug info.
- Mazoku Reminder → Detects 'Refreshing Box Opened' from Mazoku bot and pings the claimer after 60s.

## Debugging
- Prints Mazoku's raw message content and embeds into logs.
- Helps find where the 'Claimed by @user' is located.

## Deployment
1. Add your DISCORD_TOKEN and DISCORD_GUILD_ID in Railway environment variables.
2. Deploy normally.
