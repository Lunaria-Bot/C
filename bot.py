import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Mazoku bot ID
MAZOKU_ID = 1242388858897956906

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔗 Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# --- EMBED COMMAND ---
@bot.tree.command(name="embed", description="Create a custom embed with options", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(title="Embed title", description="Embed description", color="Hex color (ex: #ff0000)", footer="Footer text", thumbnail="Thumbnail URL", image="Main image URL")
async def embed(interaction: discord.Interaction, title: str, description: str, color: str = "#5865F2", footer: str = None, thumbnail: str = None, image: str = None):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

    try:
        embed_color = int(color.replace("#", ""), 16)
    except:
        embed_color = 0x5865F2

    emb = discord.Embed(title=title, description=description, color=embed_color)

    if footer:
        emb.set_footer(text=footer)
    if thumbnail:
        emb.set_thumbnail(url=thumbnail)
    if image:
        emb.set_image(url=image)

    await interaction.response.send_message(embed=emb)

# --- SAY COMMAND ---
@bot.tree.command(name="say", description="Make the bot say something", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(message="The message you want the bot to say")
async def say(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

    await interaction.response.send_message(f"✅ Sent!", ephemeral=True)
    await interaction.channel.send(message)

# --- DEBUG COMMAND ---
@bot.tree.command(name="debug", description="Debug info", guild=discord.Object(id=GUILD_ID))
async def debug(interaction: discord.Interaction):
    emb = discord.Embed(title="🔍 Debug Info", color=0x9b59b6)
    emb.add_field(name="Bot User", value=bot.user, inline=False)
    emb.add_field(name="Guild", value=interaction.guild.name, inline=False)
    emb.add_field(name="Guild ID", value=interaction.guild.id, inline=False)
    emb.add_field(name="Latency", value=f"{round(bot.latency*1000)}ms", inline=False)
    await interaction.response.send_message(embed=emb, ephemeral=True)

# --- MAZOKU REMINDER SYSTEM ---
@bot.event
async def on_message(message: discord.Message):
    if message.author.id == MAZOKU_ID and "Refreshing Box Opened" in message.content:
        # Trouver qui a claim
        for mention in message.mentions:
            user = mention
            await message.channel.send(f"⏳ Reminder set for {user.mention}! You can open again in 60s.")
            
            await asyncio.sleep(60)
            await message.channel.send(f"🎉 {user.mention} You can open again your Refreshing Box!")

    await bot.process_commands(message)

bot.run(TOKEN)
