import discord, os
import asyncio
from discord import message
from discord.ext import commands
import random

import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

game = discord.Game("KAIST 모집")
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game)
client = discord.Client()


@bot.command(name='feedback', help='Ask person for feedback')
async def shop(ctx):
    embed = discord.Embed(title="SHOP BOT",description="SHOP 아이템 목록. 쇼핑을 합시다", color=0x00aaaa)
    embed.add_field(name="STEP", value="빠르게 이동한다", inline=False)
    embed.add_field(name="STUN", value="스턴!", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🦶") #step
    await msg.add_reaction("⚔️") #stun

@client.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None
    if str(reaction.emoji) == "🦶":
        await reaction.message.channel.send(user.name + "님이 step 아이템을 구매")
    if str(reaction.emoji) == "⚔️":
        await reaction.message.channel.send(user.name + "님이 stun 아이템을 구매")

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

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return
            
@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def dice(ctx, number:int):
    await ctx.send(f'주사위를 굴려서 {random.randint(1, int(number))}이 나왔습니다')

@bot.command()
async def name(ctx):
    await ctx.send(f'author : {str(ctx.message.author)}')
    await ctx.send(f'user : {str(ctx.message.author.user)}')
    await ctx.send(f'user id : {str(ctx.message.author.user.id)}')
    await ctx.send(f'name : {str(ctx.message.author.name)}')

@bot.command(aliases=['가위바위보'])
async def rsp(ctx, number:int):
    await ctx.send(f'주사위를 굴려서 {random.randint(1, int(number))}이 나왔습니다')

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Naco Bot", description="Made bt Naco#0801", color=0x4432a8)
    embed.add_field(name="1. Hello", value="!hello", inline=False)
    embed.add_field(name="2. Dice", value="!dice [int]", inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("<:ranker:875330517166338098>")

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

@bot.command()
async def firebase_history(ctx, account_num, match_num):

    author = str(ctx.message.author)
    if author == "Naco#0801":
        name = "Naco"
    elif author == "Editor AlriC#9874":
        name = "Editor AlriC"

    cred_json = OrderedDict()
    cred_json["type"] = os.environ["type"]
    cred_json["project_id"] = os.environ["project_id"]
    cred_json["private_key_id"] = os.environ["private_key_id"]
    cred_json["private_key"] = os.environ["private_key"].replace('\\n', '\n')
    cred_json["client_email"] = os.environ["client_email"]
    cred_json["client_id"] = os.environ["client_id"]
    cred_json["auth_uri"] = os.environ["auth_uri"]
    cred_json["token_uri"] = os.environ["token_uri"]
    cred_json["auth_provider_x509_cert_url"] = os.environ["auth_provider_x509_cert_url"]
    cred_json["client_x509_cert_url"] = os.environ["client_x509_cert_url"]

    JSON = json.dumps(cred_json)
    JSON = json.loads(JSON)

    cred = credentials.Certificate(JSON)
    firebase_admin.initialize_app(cred,{
        'databaseURL' : os.environ["databaseURL"]
    })

    dir_account_battletag = db.reference(f'battle_tag/{name}/{account_num}')
    dir_score_flx = db.reference(f'score/{name}/{account_num}/flx/{match_num}')
    dir_score_tnk = db.reference(f'score/{name}/{account_num}/tnk/{match_num}')
    dir_score_dps = db.reference(f'score/{name}/{account_num}/dps/{match_num}')
    dir_score_sup = db.reference(f'score/{name}/{account_num}/sup/{match_num}')

    embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"현재 사용자 : {ctx.message.author.name}", color=0x4432a8)
    embed.add_field(name=f"{dir_account_battletag.get()}", value=f"{tier(dir_score_flx.get())} FLX {dir_score_flx.get()}\n{tier(dir_score_tnk.get())} TNK {dir_score_tnk.get()}\n{tier(dir_score_dps.get())} DPS {dir_score_dps.get()}\n{tier(dir_score_sup.get())} SUP {dir_score_sup.get()}", inline=True)
    message = await ctx.send(embed=embed)

@bot.command(aliases=['입력'])
async def input(ctx, new_score):

    # with open('data.json') as f:
    #     json_object = json.load(f)

    # account_num = 0
    # current_position = "flx"

    # author = str(ctx.message.author)
    # account_battletag = json_object['battle_tag'][author][account_num]

    # dict_len = len(json_object['score'][author][account_num][current_position])
    # len_tnk = len(json_object['score'][author][account_num]['tnk'])
    # len_dps = len(json_object['score'][author][account_num]['dps'])
    # len_sup = len(json_object['score'][author][account_num]['sup'])

    # score_flx = int(new_score)

    # score_tnk = json_object['score'][author][account_num]['tnk'][len_tnk]
    # score_dps = json_object['score'][author][account_num]['dps'][len_dps]
    # score_sup = json_object['score'][author][account_num]['sup'][len_sup]

    # json_object['score'][author][account_num][current_position][dict_len + 1] = int(new_score)

    # with open('data.json', 'w') as json_file:
    #     json.dump(json_object, json_file)

    author = str(ctx.message.author)
    if author == "Naco#0801":
        name = "Naco"
    elif author == "Editor AlriC#9874":
        name = "Editor AlriC"

    cred_json = OrderedDict()
    cred_json["type"] = os.environ["type"]
    cred_json["project_id"] = os.environ["project_id"]
    cred_json["private_key_id"] = os.environ["private_key_id"]
    cred_json["private_key"] = os.environ["private_key"].replace('\\n', '\n')
    cred_json["client_email"] = os.environ["client_email"]
    cred_json["client_id"] = os.environ["client_id"]
    cred_json["auth_uri"] = os.environ["auth_uri"]
    cred_json["token_uri"] = os.environ["token_uri"]
    cred_json["auth_provider_x509_cert_url"] = os.environ["auth_provider_x509_cert_url"]
    cred_json["client_x509_cert_url"] = os.environ["client_x509_cert_url"]

    JSON = json.dumps(cred_json)
    JSON = json.loads(JSON)

    cred = credentials.Certificate(JSON)
    firebase_admin.initialize_app(cred,{
        'databaseURL' : os.environ["databaseURL"]
    })

    dir = db.reference()
    dir.update({'hello':'test'})
    
    await ctx.send(f'Hello, {ctx.author.mention}!')

    #embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"현재 사용자 : {ctx.message.author.name}", color=0x4432a8)
    #embed.add_field(name=f"{account_battletag}", value=f"{tier(score_flx)} FLX {score_flx}\n{tier(score_tnk)} TNK {score_tnk}\n{tier(score_dps)} DPS {score_dps}\n{tier(score_sup)} SUP {score_sup}\nUpdated!", inline=True)
     
bot.run(os.environ['token'])