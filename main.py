
import discord
import random
import sqlite3
from discord import app_commands
from discord.ext import commands
import time
from datetime import datetime, timedelta

TOKEN = 'BOT_TOKEN_HERE'
GIF_URLS = [
    'https://tenor.com/bvnhs.gif',
    'https://tenor.com/m2etiAOdeyD.gif',
    'https://tenor.com/bb6Wk.gif'
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

start_time = time.time()

# Database setup
conn = sqlite3.connect("bot_stats.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, commands_ran_today INTEGER)")
c.execute("INSERT INTO stats (id, commands_ran_today) SELECT 1, 0 WHERE NOT EXISTS (SELECT 1 FROM stats WHERE id = 1)")
conn.commit()

def get_commands_ran_today():
    c.execute("SELECT commands_ran_today FROM stats WHERE id = 1")
    return c.fetchone()[0]

def update_commands_ran_today():
    c.execute("UPDATE stats SET commands_ran_today = commands_ran_today + 1 WHERE id = 1")
    conn.commit()

def get_uptime():
    return str(timedelta(seconds=int(time.time() - start_time)))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.CustomActivity(name='Try /Gangnamstyle'))

@bot.tree.command(name='stats', description='Shows bot statistics')
async def stats(interaction: discord.Interaction):
    commands_ran_today = get_commands_ran_today()
    embed = discord.Embed(title="Bot Stats", color=discord.Color.green())
    embed.add_field(name="Uptime", value=get_uptime(), inline=False)
    embed.add_field(name="Commands Ran Today", value=str(commands_ran_today), inline=False)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=False)
    embed.add_field(name="Users", value=sum(g.member_count for g in bot.guilds if g.member_count), inline=False)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        update_commands_ran_today()

@bot.tree.command(name='gangnamstyle', description='Sends a Gangnam Style GIF')
async def gangnamstyle(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(GIF_URLS))

bot.run(TOKEN)
