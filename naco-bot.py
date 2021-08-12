import discord, os
from discord import message
from discord.ext import commands
import random

import hashlib, binascii
# from Crypto.Cipher import AES

import json

game = discord.Game("404 Not Found")
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game)

def tier(score_int):
    if int(score_int) < 1500:
        return "<:bronze:875330246075891752>"
    elif 1500 <= int(score_int) < 2000:
        return "<:silver:875330313256054804>"
    elif 2000 <= int(score_int) < 2500:
        return "<:gold:875330342637158440>"
    elif 2500 <= int(score_int) < 3000:
        return "<:platinum:875330374656466994>"
    elif 3000 <= int(score_int) < 3500:
        return "<:diamond:875330418424041503>"
    elif 3500 <= int(score_int) < 4000:
        return "<:master:875330454998368266>"
    elif 4000 <= int(score_int):
        return "<:grandmaster:875330489525862470>"

def f_sha512(ctx):
    return hashlib.sha512(str(ctx).encode("utf-8")).hexdigest()

def f_pbkdf2(mess, salt, itr):
    dk = hashlib.pbkdf2_hmac('sha256', f'{str(mess).encode("utf-8")}', f'{str(salt).encode("utf-8")}', int(itr))
    return binascii.hexlify(dk)

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1:
        return None
    if str(reaction.emoji) == "\U0001F600":
        await reaction.message.send(f'{user.name} pressed \U0001F600')

@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def dice(ctx, number:int):
    await ctx.send(f'주사위를 굴려서 {random.randint(1, int(number))}이 나왔습니다')

@bot.command()
async def sha512(ctx):
    await ctx.send(f'Output : {f_sha512(ctx)}')

@bot.command()
async def pbkdf2(ctx):
    dk2 = hashlib.pbkdf2_hmac('sha256', b'testMessage', b'testSalt', 100004)
    await ctx.send(f'{binascii.hexlify(dk2)}')

@bot.command()
async def fpbkdf2(ctx, mess, salt, itr):
    await ctx.send(f'Output : {f_pbkdf2(mess, salt, itr)}')

@bot.command()
async def abcpbkdf2(ctx):
    await ctx.send(f'Output : {f_pbkdf2("testMessage", "testSalt", 100004)}')

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="PlusIdentity", description="PlusIdentity Discord Bot by Young", color=0x4432a8)
    embed.add_field(name="1. Hello", value="!hello", inline=False)
    embed.add_field(name="2. Dice", value="!dice [int]", inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("\U0001F600")

@bot.command(aliases=['기록'])
async def history(ctx, account_num, match_num):
    with open('data.json') as f:
        json_object = json.load(f)
    
    author = str(ctx.message.author)
    account_battletag = json_object['battle_tag'][author][account_num]
    score_flx = json_object['score'][author][account_num]['flx'][match_num]
    score_tnk = json_object['score'][author][account_num]['tnk'][match_num]
    score_dps = json_object['score'][author][account_num]['dps'][match_num]
    score_sup = json_object['score'][author][account_num]['sup'][match_num]

    embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"현재 사용자 : {ctx.message.author.name}", color=0x4432a8)
    embed.add_field(name=f"{account_battletag}", value=f"{tier(score_flx)} FLX {score_flx}\n{tier(score_tnk)} TNK {score_tnk}\n{tier(score_dps)} DPS {score_dps}\n{tier(score_sup)} SUP {score_sup}", inline=True)
    message = await ctx.send(embed=embed)

@bot.command(aliases=['입력'])
async def input(ctx, new_score):
    with open('data.json') as f:
        json_object = json.load(f)

    account_num = 0
    current_position = "flx"

    author = str(ctx.message.author)
    account_battletag = json_object['battle_tag'][author][account_num]

    dict_len = len(json_object['score'][author][account_num][current_position])
    len_tnk = len(json_object['score'][author][account_num]['tnk'])
    len_dps = len(json_object['score'][author][account_num]['dps'])
    len_sup = len(json_object['score'][author][account_num]['sup'])

    score_flx = int(new_score)

    score_tnk = json_object['score'][author][account_num]['tnk'][len_tnk]
    score_dps = json_object['score'][author][account_num]['dps'][len_dps]
    score_sup = json_object['score'][author][account_num]['sup'][len_sup]

    json_object['score'][author][account_num][current_position][dict_len + 1] = int(new_score)

    with open('data.json', 'w') as json_file:
        json.dump(json_object, json_file)
    

    embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"현재 사용자 : {ctx.message.author.name}", color=0x4432a8)
    embed.add_field(name=f"{account_battletag}", value=f"{tier(score_flx)} FLX {score_flx}\n{tier(score_tnk)} TNK {score_tnk}\n{tier(score_dps)} DPS {score_dps}\n{tier(score_sup)} SUP {score_sup}\nUpdated!", inline=True)
     
bot.run(os.environ['token'])