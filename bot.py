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

# ========== Events ==========
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")
    print("🔗 Commands synced")

# ========== Mazoku Detection ==========
@bot.event
async def on_message(message: discord.Message):
    # Ignore own messages
    if message.author.id == bot.user.id:
        return

    # Mazoku bot ID
    if message.author.id == 1242388858897956906:
        if message.embeds:
            for embed in message.embeds:
                print("Mazoku embed title:", embed.title)
                print("Mazoku embed description:", embed.description)

                # Detect Refreshing Box
                if embed.title and "Refreshing Box Opened" in embed.title:
                    claimed_user = None

                    # Check for "Claimed By" in description
                    if embed.description and "Claimed By" in embed.description:
                        claimed_user = embed.description.split("Claimed By")[-1].strip()

                    if claimed_user:
                        await message.channel.send(
                            f"⏳ Reminder started for {claimed_user}, you'll be pinged in 60s!"
                        )
                        await asyncio.sleep(60)
                        await message.channel.send(
                            f"🔔 {claimed_user} You can open again your Refreshing Box!"
                        )

    # Keep commands working
    await bot.process_commands(message)

# ========== Test Command ==========
@bot.tree.command(name="testembed", description="Simulate a Mazoku Refreshing Box embed", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="The user to claim the box", delay="Delay in seconds before reminder")
async def testembed(interaction: discord.Interaction, user: discord.Member, delay: int = 60):
    embed = discord.Embed(
        title="Refreshing Box Opened",
        description=f"Claimed By {user.mention}",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(delay)
    await interaction.channel.send(f"🔔 {user.mention} You can open again your Refreshing Box!")

bot.run(TOKEN)
