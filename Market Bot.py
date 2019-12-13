# bot.py
import os
import discord
import sqlite3
from database import MarketDatabase
from discord.ext import commands

db = MarketDatabase()
TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

bot = commands.Bot(command_prefix='!')
print('bot created')
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    categories = '\n - '.join([cat.name for cat in guild.categories])
    print(f'Categories:\n - {categories}')
    db.check_users()

@bot.event
async def on_member_join(member):
    db.update_user(member.name, 1, 0)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Free Market Discord server!'
    )

@bot.command(name='create_new_shop', help='Creates a new private text channel')
async def create_new_shop(ctx, name):
    user_data = db.get_user(ctx.message.author.name)
    print(user_data)
    if user_data["rank"] == user_data["num_shops"]:
        ctx.send("You have reached the maximum number of shops you can own")
        return
    else:
        user_data["num_shops"] = user_data["num_shops"] + 1
        cat = discord.utils.get(ctx.guild.categories, name="Front Page")
        db.update_user(user_data)
        await ctx.message.guild.create_text_channel(name, category=cat)
        await ctx.send(f'New text channel {name} created!')
        await ctx.send(f"You now have {user_data['num_shops']}/{user_data['rank']} shops")

@bot.command(name='info', help='Lists your information')
async def list_info(ctx):
    user_data = db.get_user(ctx.message.author.name)
    await ctx.send(f"Rank: {user_data['rank']}")
    await ctx.send(f"Shops: {user_data['num_shops']}/{user_data['rank']}")
bot.run(TOKEN)

