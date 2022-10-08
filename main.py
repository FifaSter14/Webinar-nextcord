from nextcord.ext import commands
from random import randint,choice
from typing import Optional
from time import sleep
import nextcord 
import os

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot się odpalił')
    await bot.change_presence(activity=nextcord.Game(name='Kupice patronite łysego'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def send_arg(ctx, *,arg):
    await ctx.send(arg)

@bot.command()
async def send_embed(ctx):
    embed=nextcord.Embed(title=f"Witaj {ctx.author.name}", color=0xff0000)
    await ctx.send(embed=embed)


@bot.command(aliases=["baned","zbanuj"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason='nie podano powodu'):
    await member.ban(reason=reason)
    embed=nextcord.Embed(title=f"Użytkownik {member} dostał ban za {reason}", color=0x00ffb3)
    await ctx.send(embed=embed)


@bot.command(aliases=["kicked"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: nextcord.Member, *, reason='nie podano powodu'):
    await member.kick(reason=reason)
    embed=nextcord.Embed(title=f"Użytkownik {member} dostał kicka", color=0x00ffb3)
    await ctx.send(embed=embed)


@bot.slash_command(guild_ids=[1027652135032197220],description='Random number')
async def random_number(
    interaction: nextcord.Interaction,
    min: Optional[int] = nextcord.SlashOption(required=True),
    max: Optional[int] = nextcord.SlashOption(required=True)
    ,):
    await interaction.response.send_message(randint(min,max))

@bot.event
async def on_member_join(member: nextcord.Member):
    role = nextcord.utils.get(member.guild.roles, id=1027942129105915976)
    channel = bot.get_channel(1027661092035502171)
    embed =  nextcord.Embed(description=f'Witamy {member.mention}', color=0x0bf9f9)
    await member.add_roles(role)
    await channel.send(embed=embed)

@bot.command()
async def verify(ctx):
    msg= await ctx.send('Kliknij w emotke żeby się zweryfikować')
    await msg.add_reaction('✅')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1027948200063152188:
        if payload.emoji.name == '✅':
            guild= bot.get_guild(payload.guild_id)
            member= guild.get_member(payload.user_id)
            rola=nextcord.utils.get(guild.roles, id=1027942129105915976)
            await member.add_roles(rola)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1027948200063152188:
        if payload.emoji.name == '✅':
            guild= bot.get_guild(payload.guild_id)
            member= guild.get_member(payload.user_id)
            rola=nextcord.utils.get(guild.roles, id=1027942129105915976)
            await member.remove_roles(rola)



@ban.error 
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Nie podałeś agumentu do komendu ban')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nie masz uprawnień do banowania')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Nie podałeś agumentu')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nie masz uprawanień żeby wykonać komende')
    

  
@bot.event
async def on_message(message):
    black_list=['php','frontend','discord.gg']
    for i in black_list:
        if i == message.content:
            await message.delete()
            await message.channel.send('Użyełeś słowa na liście zakazanych')
    
    await bot.process_commands(message)











bot.run('MTAyNzY1MjMxNTA5Nzg1ODA4OA.GiZlDc.Sp4PTomLEn0wlDC8FlRXoRT5t1TK1W0dJ0BO_E')