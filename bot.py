import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔗 Synced {len(synced)} commands (guild scoped)")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# Listener Mazoku messages
@bot.event
async def on_message(message: discord.Message):
    if message.author.id != 1242388858897956906:
        return

    print(f"DEBUG Mazoku message content: {message.content}")

    if message.embeds:
        for embed in message.embeds:
            print("DEBUG Mazoku embed title:", embed.title)
            print("DEBUG Mazoku embed description:", embed.description)
            print("DEBUG Mazoku embed footer:", embed.footer.text if embed.footer else None)

            if embed.title and "Refreshing Box Opened" in embed.title:
                user = None

                if embed.footer and "Opened by" in embed.footer.text:
                    footer_text = embed.footer.text
                    username = footer_text.replace("Opened by ", "").split("•")[0].strip()
                    guild = bot.get_guild(GUILD_ID)
                    user = discord.utils.find(
                        lambda m: m.name == username or m.display_name == username,
                        guild.members
                    )

                if not user:
                    for field in embed.fields:
                        if "Claimed By" in field.name and field.value:
                            user = field.value
                            break

                if user:
                    await message.channel.send(f"⏳ Reminder set for {user.mention}, you'll be pinged in 60s!")
                    await asyncio.sleep(60)
                    await message.channel.send(f"🔔 {user.mention} You can open again your Refreshing Box!")

# Command /ping pour vérifier le bot
@bot.tree.command(name="ping", description="Check if the bot is alive", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

bot.run(TOKEN)
