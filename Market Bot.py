# bot.py
import os
import discord
import sqlite3
from database import MarketDatabase
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from threading import Timer

db = MarketDatabase()
TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

bot = commands.Bot(command_prefix='/')
print('bot created')

def periodic_check():
    check_shop_expire()
    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()
    t = Timer(secs, periodic_check())
    t.start()

def check_shop_expire():
    remove_list = db.update_all_shop_durations()
    for shop in remove_list:
        channel = get(bot.guilds[0], name = shop[0])
        await channel.delete()
    announce_channel = get(bot.guilds[0], name = 'expired-shops-removal')
    formatted_list = [f"{shop[0]:<30}{shop[1]:<30}" for shop in remove_list]
    name, owner = "Name", "Owner"
    msg = "The following shops are expired and have been removed\n"
    await announce_channel.send(msg + '\n'.join([f"{name:<30}{owner:<30}"] + [""] + formatted_list))

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
    periodic_check()

@bot.event
async def on_member_join(member):
    db.update_user(member.name, 1, 0, 0)
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to the Free Market Discord server! To start browsing the market, please agree to our terms and conditions in the terms-and-conditions channel by typing \"/agree\".")

@bot.command(name='agree', help='Agree to our terms and conditions and start browsing the market')
async def agree(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, name="Customer")
    await ctx.send(f"{member.name}, you are now a member and free to browse the market")
    await member.add_roles(role)

@bot.command(name='create', help='Creates a new private text channel')
async def create(ctx, cat_brief, name):
    if len(ctx.message.author.roles) == 0:
        await ctx.send("You are not yet a member. Please type /agree to agree to our terms and conditions in order to become a member.")
        return
    user_data = db.get_user(ctx.message.author.name)
    if user_data["rank"] == user_data["num_shops"]:
        await ctx.send("You have reached the maximum number of shops you can own")
    else:
        category_name = "FM Channel 1"
        if cat_brief == "frontpage":
            VIP = get(ctx.message.guild.roles, name='VIP')
            if VIP in ctx.message.author.roles:
                category_name = "Front Page"
            else:
                await ctx.send("Only VIPs can create their shop in the front page!")
                return
        elif "ch" in cat_brief:
            category_name = "FM Channel " + cat_brief[2:]
            cat_names = [cat.name for cat in ctx.guild.categories]
            if not category_name in cat_names:
                await ctx.send(category_name + " does not exists...")
                return
        
        if(db.add_shop(name, 1, user_data["name"]) == "success"):
            cat = discord.utils.get(ctx.guild.categories, name=category_name)
            guild = ctx.message.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False)
                ctx.message.author : discord.PermissionOverwrite()
            }
            await guild.create_text_channel(name, overwrites=overwrites, category=cat)
            await ctx.send(f'New text channel {name} created!')
        else:
            await ctx.send("Shop name taken...")

@bot.command(name='remove', help='Remove one of your shops(text channels)')
async def remove(ctx, shop_name):
    if len(ctx.message.author.roles) == 0:
        await ctx.send("You are not yet a member. Please type /agree to agree to our terms and conditions in order to become a member.")
        return
    owner = ctx.message.author.name
    for channel in ctx.message.guild.channels:
        if channel.name == shop_name and db.remove_shop(shop_name, owner) == "success":
            u = db.get_user(owner)
            free_spots = u["rank"] - u["num_shops"]
            await channel.delete()
            await ctx.send(f"{shop_name} has been removed. You now have {free_spots} spot(s) for shops.")
            return
    await ctx.send(f"Can't find a shop named \"{shop_name}\"")

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

@bot.command(name='set_coins', help='Set the coins of a member to a certain number(Admin or above only)')
async def set_coins(ctx, username, coins):
    user_roles = ctx.message.author.roles
    for role in user_roles:
        if role.name == "Admin" or role.name == "CEO":
            u = db.get_user(username)
            u["coins"] = coins
            db.update_user_by_data(u)
            await ctx.send(f"{username} now has {coins} coins")
            return
    await ctx.send("You are not permitted to use this command!")

@bot.command(name='info', help='Lists your information')
async def list_info(ctx):
    name = ctx.message.author.name
    user_data = db.get_user(name)
    shops_owned = db.get_shops_owned(name)
    msgs = [f"Rank: {user_data['rank']}",
            f"Money: {user_data['coins']}",
            f"Shops: {user_data['num_shops']}/{user_data['rank']}",
            "\n",
            f"{'Name':<30}{'Days until expire':<30}"
            ]
    try:
        msgs.append(('\n'.join(f"{shop[0]:<30}{shop[1]:<30}" for shop in shops_owned)))
    except:
        pass
    await ctx.send('\n'.join(msgs))

bot.run(TOKEN)


