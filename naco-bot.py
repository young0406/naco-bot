import discord, os
from discord import message
from discord.ext import commands
import random

import json

game = discord.Game("자경 스피드패작")
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game)
client = discord.Client()

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

@client.event
async def on_reaction_add(reaction, user):
    await reaction.message.send(f'{user.name} pressed {str(reaction.emoji)}')

@bot.command(name='feedback', help='Ask person for feedback')
async def roll(ctx):
    message = await ctx.send('Are you enjoying this bot? \n :thumbsup: :-1: ')

    thumb_up = '👍'
    thumb_down = '👎'

    await message.add_reaction(thumb_up)
    await message.add_reaction(thumb_down)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [thumb_up, thumb_down]

    member = ctx.author

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=10.0, check=check)

            if str(reaction.emoji) == thumb_up:
                await ctx.send('Thank you for your feedback')


            if str(reaction.emoji) == thumb_down:
                await ctx.send('Sorry you feel that way')
        finally:
            await ctx.send('I dont know')
            
@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def dice(ctx, number:int):
    await ctx.send(f'주사위를 굴려서 {random.randint(1, int(number))}이 나왔습니다')

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