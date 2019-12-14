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

@bot.command(name='create', help='Creates a new private text channel')
async def create(ctx, name, channel_category):
    user_data = db.get_user(ctx.message.author.name)
    if user_data["rank"] == user_data["num_shops"]:
        await ctx.send("You have reached the maximum number of shops you can own")
    else:
        if(db.add_shop(name, user_data["name"]) == "success"):
            cat = discord.utils.get(ctx.guild.categories, name=channel_category)
            await ctx.message.guild.create_text_channel(name, category=cat)
            await ctx.send(f'New text channel {name} created!')
        else:
            await ctx.send("Shop name taken...")

@bot.command(name='remove', help='Remove one of your shops(text channels)')
async def remove(ctx, shop_name):
    owner = ctx.message.author.name
    if(db.remove_shop(shop_name, owner) == "success"):
        for channel in ctx.message.guild.channels:
            if channel.name == shop_name:
                u = db.get_user(owner)
                free_spots = u["rank"] - u["num_shops"]
                await channel.delete()
                await ctx.send(f"{shop_name} has been removed. You now have {free_spots} spot(s) for shops.")
                return
        ctx.send(f"Can't find a shop named {shop_name}")
    else:
        await ctx.send("Error occurred while removing shop in the database...")

@bot.command(name='set_rank', help='Set the rank of a member(Admin or above only)')
async def set_rank(ctx, username, rank):
    user_roles = ctx.message.author.roles
    for role in user_roles:
        if role.name == "Admin" or role.name == "CEO":
            u = db.get_user(username)
            u["rank"] = rank
            db.update_user_by_data(u)
            await ctx.send(f"{username}'s rank has been set to {rank}")
            return
    await ctx.send("You are not permitted to use this command!")

@bot.command(name='info', help='Lists your information')
async def list_info(ctx):
    name = ctx.message.author.name
    user_data = db.get_user(name)
    shops_owned = db.get_shops_owned(name)
    await ctx.send(f"Rank: {user_data['rank']}")
    await ctx.send(f"Shops: {user_data['num_shops']}/{user_data['rank']}")
    try:
        await ctx.send('\n'.join(shop for shop in shops_owned))
    except:
        pass
bot.run(TOKEN)

