# bot.py
import os
import requests
import youtube_dl
import json

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USERNAME = os.getenv('IMGFLIP_USERNAME')
PASS = os.getenv('IMGFLIP_PASSWORD')
RIOTAPI = os.getenv("RIOT_API")

bot = commands.Bot(command_prefix='!!')

regions = {
    'ru': "ru",
    'kr': "kr",
    'br': 'br1',
    'oc': 'oc1',
    'jp': 'jp1',
    'na': 'na1',
    'eun': 'eun1',
    'euw': 'euw1',
    'tr': 'tr1',
    'la1': 'la1',
    'la2': 'la2'
}

champion_request = requests.get('http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion.json')
champions = champion_request.json()
champions = champions['data']


def champ_namer(id):
    for champion in champions:
        if champions[champion]['key'] == str(id):
            return (champions[champion]['name'] + " " + champions[champion]['title'])


def coinchecker(coin, parabirimi):
    url = 'https://min-api.cryptocompare.com/data/pricemulti'
    parameters = {
        'fsyms': coin,
        'tsyms': parabirimi
    }
    finaltext = '```'

    r = requests.get(url=url, params=parameters)
    data = r.json()
    for key in data:
        finaltext += "\n"
        finaltext += key + " güncel piyasa değerleri\n"
        finaltext += "---------------------\n"
        for subkey in data[key]:
            finaltext += subkey + ' -> ' + str(data[key][subkey]) + "\n"

    finaltext += "```"
    return finaltext


def region_picker(argument):
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return regions.get(argument, "euw1")


def sum(name, region):
    reg = region_picker(region)
    url = "https://" + reg + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name
    HEADERS = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": RIOTAPI,
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78"
    }

    r = requests.get(url=url, headers=HEADERS)
    data = r.json()
    return data


def liginfo(id, region):
    reg = region_picker(region)
    url = "https://" + reg + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + id
    HEADERS = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": RIOTAPI,
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78"
    }

    r = requests.get(url=url, headers=HEADERS)
    data = r.json()
    return data


def masteryinfo(id, region):
    reg = region_picker(region)
    url = "https://" + reg + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + id
    HEADERS = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": RIOTAPI,
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78"
    }

    r = requests.get(url=url, headers=HEADERS)
    data = r.json()
    return data


def get_memes():
    URL = 'https://api.imgflip.com/get_memes'
    r = requests.get(URL)

    data = r.json()
    for meme in data['data']['memes']:
        print(meme['id'] + ' | ' + meme['name'] + ' | ' + meme['url'])


def create_meme(text1, text2, t_id):
    URL = 'https://api.imgflip.com/caption_image'
    data = {'template_id': t_id,
            'username': USERNAME,
            'password': PASS,
            'text0': text1,
            'text1': text2
            }
    r = requests.post(url=URL, data=data)
    data = r.json()
    return data['data']['url']


def create_meme_complex(t_id, text1, text2, text3='', text4='', text5=''):
    URL = 'https://api.imgflip.com/caption_image'
    data = {'template_id': t_id,
            'username': USERNAME,
            'password': PASS,
            'boxes[0][text]': text1,
            'boxes[1][text]': text2,
            'boxes[2][text]': text3,
            'boxes[3][text]': text4,
            'boxes[4][text]': text5,
            }
    r = requests.post(url=URL, data=data)
    data = r.json()
    return data['data']['url']


@bot.event
async def on_ready():
    print(
        f'{bot.user.name} is connected to the Discord!\n'
    )


@bot.command(name='selam', help='Selamınızı geri çevirmeyen komut', pass_context=True)
async def selamlayici(ctx):
    try:
        await ctx.send(f"Sana da selam canım nasılsın iyi misin? {ctx.message.author.mention} :heart:")
    except Exception as e:
        print(str(e))


@bot.command(name='buton', help='İki buton meme')
async def buton_meme(ctx, t1, t2):
    yazi1 = ''
    yazi2 = ''
    try:
        if t1 is not None:
            yazi1 = t1
        if t2 is not None:
            yazi2 = t2
        response = create_meme(yazi1, yazi2, 87743020)
        await ctx.send(response)
    except Exception as e:
        print(str(e))


@bot.command(name='pooh', help='Tuxedo winnie')
async def pooh_meme(ctx, t1, t2):
    yazi1 = ''
    yazi2 = ''
    try:
        if t1 is not None:
            yazi1 = t1
        if t2 is not None:
            yazi2 = t2
        response = create_meme(yazi1, yazi2, 178591752)
        await ctx.send(response)
    except Exception as e:
        print(str(e))


@bot.command(pass_context=True)
async def crypto(ctx, t1, t2):
    embedFile = discord.Embed(
        title="Crypto Market",
        description="Güncel Market Bilgileri",
        colour=discord.Colour.green())
    embedFile.set_footer(text="Crypto Market")
    embedFile.set_thumbnail(url="https://www.cryptodir.com/media/k2/categories/1.png")
    embedFile.set_author(name="KillJoyJR",
                         icon_url="https://cdn.discordapp.com/avatars/146477952534577152/bd8fb90a7e545dcd8ca945fe368f2630.png")
    response = coinchecker(t1, t2)
    embedFile.add_field(name="Piyasa Değerleri\n:moneybag:", value=response)
    await ctx.send(embed=embedFile)


@bot.command(pass_context=True)
async def summoner(ctx, t1, t2):
    suminfo = sum(t1, t2)
    mastery_list = ""
    t2 = t2.lower()
    if 'status' in suminfo:
        if 'status_code' in suminfo['status']:
            await ctx.send(suminfo['status']['message'])
            return
    if t2 not in regions:
        await ctx.send("Region not found, defaulting to EUW")
    leagueinfo = liginfo(suminfo['id'], t2)
    masteries = masteryinfo(suminfo['id'], t2)
    embedFile = discord.Embed(
        title="League of Legends",
        colour=0xf2c409)
    embedFile.set_thumbnail(
        url="http://ddragon.leagueoflegends.com/cdn/9.24.2/img/profileicon/" + str(suminfo['profileIconId']) + ".png")
    embedFile.add_field(name="Summoner Name", value=suminfo['name'], inline=True)
    embedFile.add_field(name="Region", value=t2.upper() if t2 in regions else "EUW", inline=True)
    embedFile.add_field(name="Summoner Level", value=str(suminfo['summonerLevel']), inline=False)

    if leagueinfo:
        for item in leagueinfo:
            embedFile.add_field(name=item['queueType'], value=item['tier'] + " " + item['rank'], inline=True)
            embedFile.add_field(name="League Points", value=str(item['leaguePoints']), inline=True)
            embedFile.add_field(name="Win/Lose - Winrate :fire:" if round(
                (item['wins'] / (item['wins'] + item['losses'])) * 100) >= 50 else "Win/Lose - Winrate :eggplant:",
                                value=str(item['wins']) + "/" + str(item['losses']) + " - %" + str(
                                    round((item['wins'] / (item['wins'] + item['losses'])) * 100)), inline=True)
    if masteries:
        for i in range(3):
            if masteries[i] in masteries:
                mastery_list += (champ_namer(int(masteries[i]['championId'])) + " / " + str(masteries[i]['championPoints']) + " points" + "\n\n")

        embedFile.add_field(name="Most Played Champions", value="Not enough data" if mastery_list == "" else mastery_list, inline=False)
    await ctx.send(embed=embedFile)


@bot.command(name='yellcat', help='Kediye bağırma')
async def kedi_meme(ctx, t1, t2):
    yazi1 = ''
    yazi2 = ''
    try:
        if t1 is not None:
            yazi1 = t1
        if t2 is not None:
            yazi2 = t2
        response = create_meme_complex(188390779, yazi1, yazi2)
        await ctx.send(response)
    except Exception as e:
        print(str(e))


@bot.command(name='iho', help='Imma head out')
async def iho_meme(ctx, t1):
    yazi1 = t1
    try:
        response = create_meme(yazi1, '', 196652226)
        await ctx.send(response)
    except Exception as e:
        print(str(e))


@bot.command(name='boyfriend', help='Distracted boyfriend')
async def bf_meme(ctx, t1, t2, t3):
    try:
        response = create_meme_complex(112126428, t1, t2, t3)
        await ctx.send(response)
    except Exception as e:
        print(str(e))


@bot.command(name='argument', help='American Chopper Argument')
async def argument_meme(ctx, t1, t2, t3, t4, t5):
    try:
        response = create_meme_complex(134797956, t1, t2, t3, t4, t5)
        await ctx.send(response)
    except Exception as e:
        print(str(e))

@kedi_meme.error
async def kedi_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!yellcat <yazı 1> <yazı 2>```')


@summoner.error
async def summoner_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!summoner "summoner name" "region"```')


@crypto.error
async def crypto_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Örnek Kullanım: !!crypto "BTC,ETH" "TRY,USD"```')


@bf_meme.error
async def bf_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!boyfriend <yazı 1 (Distraction)> <yazı 2 (BF)> <yazı 3 (GF)>```')


@argument_meme.error
async def argument_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!argument <yazı 1> <yazı 2> <yazı 3> <yazı 4> <yazı 5>```')


@iho_meme.error
async def iho_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!iho <yazı> ```')


@pooh_meme.error
async def pooh_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!pooh <yazı 1> <yazı 2>```')


@buton_meme.error
async def buton_meme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Kullanım: !!buton <yazı 1> <yazı 2>```')



bot.run(TOKEN)
