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
        await ctx.send("You have reached the maximum number of shops you can own")
    else:
        if(db.add_shop(name, user_data["name"]) == "success"):
            cat = discord.utils.get(ctx.guild.categories, name="Front Page")
            await ctx.message.guild.create_text_channel(name, category=cat)
            await ctx.send(f'New text channel {name} created!')
        else:
            await ctx.send("Shop name taken...")

@bot.command(name='remove_shop', help='Remove one of your shops')
async def remove_shop(ctx, shop_name):
    owner = ctx.message.author.name
    if(db.remove_shop(shop_name, owner) == "success"):
        for channel in ctx.message.guild.channels:
            if channel.name == shop_name:
                await channel.delete()
                await ctx.send(f"{shop_name} has been removed. You now have {free_spots} spots for shops.")
                break
    else:
        await ctx.send("Invalid shop name...")

@bot.command(name='info', help='Lists your information')
async def list_info(ctx):
    name = ctx.message.author.name
    user_data = db.get_user(name)
    shops_owned = db.get_shops_owned(name)
    await ctx.send(f"Rank: {user_data['rank']}")
    await ctx.send(f"Shops: {user_data['num_shops']}/{user_data['rank']}")
    await ctx.send('\n'.join(shop for shop in shops_owned))
bot.run(TOKEN)

