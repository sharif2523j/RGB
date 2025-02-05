import discord
import asyncio

# Your bot's token


# Create a client instance
intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

# Color change interval (seconds)
interval = 2.0  # 2 seconds delay to avoid hitting rate limits

# Define the colors (RGB values for red, green, blue, and pink)
colors = [
    discord.Color(0xFF0000),  # Red
    discord.Color(0x00FF00),  # Green
    discord.Color(0x0000FF),  # Blue
    discord.Color(0xFF69B4),  # Pink
]

# Function to handle role color updates with rate limit handling
async def rgb_role_color(role):
    color_index = 0

    while True:
        try:
            # Change the role color
            await role.edit(color=colors[color_index])
            print(f"Updated role color to: {colors[color_index]}")
            
            # Move to the next color in the list, looping back to the start
            color_index = (color_index + 1) % len(colors)
        except discord.errors.HTTPException as e:
            if e.code == 50035:
                print("Rate limit hit, retrying after delay...")
                retry_after = e.retry_after
                print(f"Waiting for {retry_after} seconds before retrying.")
                await asyncio.sleep(retry_after)  # Wait before retrying
            else:
                print(f"Error changing role color: {e}")
        
        # Delay between color changes
        await asyncio.sleep(interval)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')




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
