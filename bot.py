import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.environ.get("TOKEN")
GUILD_ID = os.environ.get("GUILD_ID")

if not TOKEN or not GUILD_ID:
    raise RuntimeError("❌ Missing TOKEN or GUILD_ID environment variables.")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))

@bot.tree.command(name="ping", description="Test if the bot is alive", guild=discord.Object(id=int(GUILD_ID)))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

bot.run(TOKEN)
