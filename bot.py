import discord
import asyncio

# Your bot's token
TOKEN = 'MTMwODc4MDM2MDczMzAzNjYxNQ.GE6J8O.OmcJi-j0AcrBPXoY-bMsuSTgn2L6YtoEucrcZU'

# Create a client instance
intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

# Color change interval (100ms)
interval = 0.1  # 100ms in seconds

# Generate RGB colors (example)
def generate_rgb_colors():
    colors = []
    for r in range(255, -1, -15):
        colors.append(f"#{r:02x}00ff")
    for g in range(0, 256, 15):
        colors.append(f"#ff{g:02x}00")
    for b in range(255, -1, -15):
        colors.append(f"#00ff{b:02x}")
    return colors

# Function to handle role color updates with rate limit handling
async def rgb_role_color(role):
    color_index = 0
    colors = generate_rgb_colors()

    while True:
        try:
            await role.edit(color=discord.Color(int(colors[color_index][1:], 16)))
            print(f"Updated role color to: {colors[color_index]}")
            color_index = (color_index + 1) % len(colors)
        except discord.errors.HTTPException as e:
            if e.code == 50035:
                print("Rate limit hit, retrying after delay...")
                retry_after = e.retry_after
                print(f"Waiting for {retry_after} seconds before retrying.")
                await asyncio.sleep(retry_after)  # Wait before retrying
            else:
                print(f"Error changing role color: {e}")
        await asyncio.sleep(interval)  # Delay between color changes

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    guild_id = '1276937434877132893'  # Replace with your server ID
    role_id = '1336699795481300992'    # Replace with your role ID

    guild = client.get_guild(int(guild_id))
    if guild:
        role = guild.get_role(int(role_id))
        if role:
            print(f"Found role: {role.name} (ID: {role.id})")
            await rgb_role_color(role)  # Start the color change process
        else:
            print('Role not found! Double-check your role ID.')
    else:
        print('Guild not found! Double-check your server ID.')

client.run(TOKEN)  # Log in the bot
