import requests
from datetime import datetime
import discord
from discord.ext import tasks
from tabulate import tabulate
import json

Token = 'MTE4ODIxMjAzMjM1NzUzOTg1MQ.GEgoDJ.fqmD-9bvpU0mfKsXYYUy9O3oIhArZ9nP2Gn5UI'

client = discord.Bot(intents=discord.Intents.default())

Black, Purple, Blue, Green, Yellow, Red, Orange, SolCol = 0x00000, 0xA020F0, 0x0000FF, 0x00FF00, 0xFFFF33, 0xFF0000, 0xFFA500, 0x03E1FF

Footer = 'Powered by LoLo Labs'
ImageURL = 'https://iili.io/HPgfNmF.png'
FooterImg = 'https://iili.io/HPgfWgV.png'
AuthorName = 'Solana Volume'

def Report(TF):
    C = 0
    #Ranking = ['🥇', '🥈', '🥉', '🥉', '🥉', '🥉', '🥉', '🥉', '🥉', '🥉', '🥉']
    Ranking = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    Main = []
    response = requests.get(
        f'https://solanaapi.nftscan.com/api/sol/statistics/ranking/trade?time={TF}&sort_field=volume&sort_direction=desc',
        headers={'X-API-KEY': 'UpHv9E2zqy9TValq6VhoRUXd'})
        # headers={'X-API-KEY': 'oWZhEOcSOYEopEpLnHGYzx9I'})

    print(response.text)
    for i in json.loads(response.text)['data']:
        if i['floor_price'] is not None and i["contract_name"] is not None and i['volume'] is not None:
            List = []
            List.append(Ranking[C])
            List.append(f'{i["contract_name"][0:20]}')
            List.append(i['sales'])
            List.append(round(i['volume'], 2))
            List.append(round(i['lowest_price'], 2))
            List.append(round(i['highest_price'], 2))
            C += 1
            Main.append(List)
            if C == 10:
                ModifiedMain = Main
                Columns = ["#", "Collection", "Sold", "Volume", "Low", "High"]
                Table = (tabulate(ModifiedMain, headers=Columns, numalign="center", stralign="left"))
                return Table

@client.event
async def on_ready():
    print(f"We have logged in as {client.user} Commands")
    Market15m.start()
    Market30m.start()
    Market1hr.start()
    Market1d.start()

@tasks.loop(minutes=15)
async def Market15m():
    SalesVol = discord.Embed(title=f'📈 Popular Collections | 15M',
                             description=f'```{Report("15m")}```', color=Purple)
    SalesVol.set_author(name=AuthorName, icon_url=ImageURL)
    SalesVol.set_footer(text=Footer, icon_url=FooterImg)

    try:
        Channel = await client.fetch_channel(1188211884357337208)
        await Channel.send(embed=SalesVol)
    except:
        pass

@tasks.loop(minutes=30)
async def Market30m():
    SalesVol = discord.Embed(title=f'📈 Popular Collections | 30M',
                        description=f'```{Report("30m")}```', color=Purple)
    SalesVol.set_author(name=AuthorName, icon_url=ImageURL)
    SalesVol.set_footer(text=Footer, icon_url=FooterImg)

    try:
        Channel = await client.fetch_channel(1188213151695638598)
        await Channel.send(embed=SalesVol)
    except:
        pass

@tasks.loop(hours=1)
async def Market1hr():
    SalesVol = discord.Embed(title=f'📈 Popular Collections | 1H',
                        description=f'```{Report("1h")}```', color=Purple)
    SalesVol.set_author(name=AuthorName, icon_url=ImageURL)
    SalesVol.set_footer(text=Footer, icon_url=FooterImg)

    try:
        Channel = await client.fetch_channel(1188213281446449292)
        await Channel.send(embed=SalesVol)
    except:
        pass

@tasks.loop(hours=1)
async def Market1d():
    now = datetime.now()
    if '00' in now.strftime("%H"):

        SalesVol = discord.Embed(title=f'📈 Popular Collections | 1D',
                            description=f'```{Report("1d")}```', color=Purple)
        SalesVol.set_author(name=AuthorName, icon_url=ImageURL)
        SalesVol.set_footer(text=Footer, icon_url=FooterImg)

        try:
            Channel = await client.fetch_channel(1188213321447522436)
            await Channel.send(embed=SalesVol)
        except:
            pass

client.run(Token)