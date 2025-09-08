import os
import discord
from discord.ext import commands
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
MAZOKU_ID = 1242388858897956906

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

debug_user = None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔗 Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="debugmode", description="Enable Mazoku debug logs via DM", guild=discord.Object(id=GUILD_ID))
async def debugmode(interaction: discord.Interaction):
    global debug_user
    debug_user = interaction.user
    await interaction.response.send_message("✅ Debug mode enabled! I'll DM you Mazoku messages.", ephemeral=True)

@bot.tree.command(name="stopdebug", description="Disable Mazoku debug logs", guild=discord.Object(id=GUILD_ID))
async def stopdebug(interaction: discord.Interaction):
    global debug_user
    debug_user = None
    await interaction.response.send_message("🛑 Debug mode disabled.", ephemeral=True)

@bot.event
async def on_message(message: discord.Message):
    global debug_user

    if message.author.id == MAZOKU_ID:
        print("DEBUG Mazoku message content:", message.content)

        if debug_user:
            try:
                dm_content = f"**Mazoku message content:** `{message.content}`\n"
                if message.embeds:
                    for i, embed in enumerate(message.embeds):
                        embed_dict = embed.to_dict()
                        dm_content += f"**Embed #{i}:** ```json\n{embed_dict}```\n"
                await debug_user.send(dm_content[:1900])
            except Exception as e:
                print("⚠️ Could not DM debug info:", e)

        text_to_check = message.content
        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    text_to_check += " " + embed.description
                if embed.title:
                    text_to_check += " " + embed.title

        if "Refreshing Box Opened" in text_to_check:
            if message.mentions:
                for user in message.mentions:
                    await message.channel.send(f"⏳ Reminder set for {user.mention}! You can open again in 60s.")
                    await asyncio.sleep(60)
                    await message.channel.send(f"🎉 {user.mention} You can open again your Refreshing Box!")
            else:
                await message.channel.send("⚠️ Could not detect the player mention in Mazoku's message.")

    await bot.process_commands(message)

bot.run(TOKEN)
