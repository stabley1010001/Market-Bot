# bot.py
import os
import discord
from discord.ext import commands

f = open('info.txt', 'r')
lines = f.readlines
TOKEN = lines[0]
GUILD = lines[1]
f.close()

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

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Free Market Discord server!'
    )


@bot.command(name='create_new_shop', help='Creates a new private text channel')
async def create_new_shop(ctx, name):
    cat = discord.utils.get(ctx.guild.categories, name="Front Page")
    await ctx.message.guild.create_text_channel(name, category=cat)
    await ctx.send(f'New text channel {name} created!')

bot.run(TOKEN)

