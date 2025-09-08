import os
import json
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD_ID = os.environ.get("DISCORD_GUILD_ID")

if not TOKEN or not GUILD_ID:
    raise RuntimeError("❌ Missing DISCORD_TOKEN or DISCORD_GUILD_ID environment variables.")

GUILD_ID = int(GUILD_ID)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

STORAGE_FILE = "storage.json"

def load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {"autoroles": {}}
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

storage = load_storage()

class AutoroleButton(discord.ui.Button):
    def __init__(self, role_id: int):
        super().__init__(style=discord.ButtonStyle.primary, label="Get Role", custom_id=f"autorole-{role_id}")
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if not role:
            await interaction.response.send_message("❌ Role not found.", ephemeral=True)
            return

        member = interaction.user
        try:
            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"❌ Removed {role.name}.", ephemeral=True)
            else:
                await member.add_roles(role)
                await interaction.response.send_message(f"✅ You got {role.name}!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ I don’t have permission to manage this role.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Logged in as {bot.user}")

    for msg_id, data in storage["autoroles"].items():
        channel = bot.get_channel(data["channel_id"])
        if channel:
            view = discord.ui.View(timeout=None)
            view.add_item(AutoroleButton(data["role_id"]))
            bot.add_view(view, message_id=int(msg_id))

@bot.tree.command(name="ping", description="Test if the bot is alive", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="embed", description="Create a custom embed with options", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def embed(interaction: discord.Interaction, title: str, description: str, color: str = "blue", thumbnail: str = None, image: str = None):
    try:
        if color.startswith("#"):
            embed_color = discord.Color(int(color[1:], 16))
        else:
            colors = {
                "red": discord.Color.red(),
                "blue": discord.Color.blue(),
                "green": discord.Color.green(),
                "yellow": discord.Color.yellow(),
                "purple": discord.Color.purple(),
                "orange": discord.Color.orange()
            }
            embed_color = colors.get(color.lower(), discord.Color.blurple())
    except:
        embed_color = discord.Color.blurple()

    emb = discord.Embed(title=title, description=description, color=embed_color)
    if thumbnail and thumbnail.startswith("http"):
        emb.set_thumbnail(url=thumbnail)
    if image and image.startswith("http"):
        emb.set_image(url=image)

    await interaction.response.send_message(embed=emb)

@bot.tree.command(name="autorole", description="Send an auto role message", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def autorole(interaction: discord.Interaction, role: discord.Role):
    button = AutoroleButton(role.id)
    view = discord.ui.View(timeout=None)
    view.add_item(button)
    msg = await interaction.channel.send(
        content=f"Click below to get the **{role.name}** role:",
        view=view
    )
    await interaction.response.send_message("✅ Autorole message created.", ephemeral=True)
    storage["autoroles"][str(msg.id)] = {"channel_id": interaction.channel.id, "role_id": role.id}
    save_storage(storage)

@bot.tree.command(name="say", description="Make the bot say something", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None, embed: bool = False):
    target_channel = channel or interaction.channel
    if embed:
        emb = discord.Embed(description=message, color=discord.Color.blurple())
        await target_channel.send(embed=emb)
    else:
        await target_channel.send(message)
    await interaction.response.send_message(f"✅ Message sent in {target_channel.mention}", ephemeral=True)

@bot.tree.command(name="debug", description="Show bot debug info", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def debug(interaction: discord.Interaction):
    guild = interaction.guild
    emb = discord.Embed(title="🛠️ Debug Info", color=discord.Color.blurple())
    emb.add_field(name="Bot", value=f"{bot.user} (`{bot.user.id}`)", inline=False)
    emb.add_field(name="Server", value=f"{guild.name} (`{guild.id}`)", inline=False)
    emb.add_field(name="Members", value=str(guild.member_count), inline=True)
    emb.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
    emb.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
    emb.add_field(name="Intents", value=f"Members: {bot.intents.members}\nGuilds: {bot.intents.guilds}", inline=False)
    await interaction.response.send_message(embed=emb, ephemeral=True)

@embed.error
@autorole.error
@say.error
@debug.error
async def permissions_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You must be an **Administrator** to use this command.", ephemeral=True)

bot.run(TOKEN)
