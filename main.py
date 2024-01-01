import requests
from datetime import datetime
import discord
from discord.ext import tasks
from tabulate import tabulate
import json

Token = 'MTE4ODIxMjAzMjM1NzUzOTg1MQ.GEgoDJ.fqmD-9bvpU0mfKsXYYUy9O3oIhArZ9nP2Gn5UI'

client = discord.Bot(intents=discord.Intents.default())

Black, Purple, Blue, Green, Yellow, Red, Orange, SolCol = 0x00000, 0xA020F0, 0x0000FF, 0x00FF00, 0xFFFF33, 0xFF0000, 0xFFA500, 0x03E1FF

Footer = 'Powered by Pyro'
ImageURL = 'https://pyro-nft.vercel.app/logo-pyro.png'
FooterImg = 'https://pyro-nft.vercel.app/logo-pyro.png'
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
    data = json.loads(response.text)['data']
    print(f"Number of elements from API: {len(data)}")

    for i in data:
        floor_price = i.get('lowest_price')
        contract_name = i.get("collection")
        volume = i.get('volume')
        print(f"Checking for collection: {i.get('collection')}")
        print(f"floor_price: {floor_price}, contract_name: {contract_name}, volume: {volume}")

        if contract_name and volume is not None:  # Modification de la condition ici
            List = [Ranking[C], contract_name[:20], i.get('sales'), round(volume, 2)]

            List.append(round(floor_price, 2) if floor_price is not None else 'N/A')
            List.append(round(i['highest_price'], 2))


            C += 1
            Main.append(List)
            
            
            if C == 10:
                break
    
    if Main:
        Columns = ["#", "Collection", "Sold", "Volume", "Low", "High"]
        Table = tabulate(Main, headers=Columns, numalign="center", stralign="left")
        return Table
    else:
        return "No data available."

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
        Channel = await client.fetch_channel(1191440716568739931)
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
        Channel = await client.fetch_channel(1191442846398558278)
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
        Channel = await client.fetch_channel(1191442883950149722)
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
            Channel = await client.fetch_channel(1191455785939632139)
            await Channel.send(embed=SalesVol)
        except:
            pass

client.run(Token)