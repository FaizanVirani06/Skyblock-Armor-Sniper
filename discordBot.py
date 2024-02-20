from configparser import InterpolationMissingOptionError
import discord
import requests
from discord.ext import commands
from discord.ext import tasks
import time
import asyncio

mods = ""
client = commands.Bot(command_prefix = ("s!"))

@client.event
async def on_ready():
    print("The bot is online!\n------------------------------")
    notifier.start()
    print("notifier started")

@client.command()
async def pause(ctx, a):
    global waiting
    waiting = True
    await asyncio.sleep(int(a))
    waiting = False
        
@client.command()
async def stop(ctx):
    global stopa 
    stopa = True

@client.command()
async def apiremove(ctx, api):
    global waiting
    waiting = True
    if ctx.author.id != 816924533037596682:
        embed=discord.Embed(description="Only step can do that!", color=0xFF0000)
        try:
            await ctx.channel.send(embed=embed)
        except:
            print()
    with open("apikeys.txt", "r") as r:
        apis = r.readlines()
    if (api) in apis:
        for i in range(len(apis)):
            if api in apis[i]:
                del apis[i]
                embed=discord.Embed(description="API key removed!", color=0x00FF00)
        await ctx.channel.send(embed=embed)
        with open("apikeys.txt", "w") as r:
            print()
        with open("apikeys.txt", "a") as r:
            for i in apis:
                r.write(i.strip() + "\n")
    else:
        embed=discord.Embed(description="That API key was not found...", color=0xFF0000)
        await ctx.channel.send(embed=embed)
    waiting = False

async def apir(api):
    with open("apikeys.txt", "r") as r:
        apis = r.readlines()
    if (api) in apis:
        for i in range(len(apis)):
            if api in apis[i]:
                del apis[i]
        with open("apikeys.txt", "w") as r:
            print()
        with open("apikeys.txt", "a") as r:
            for i in apis:
                r.write(i.strip() + "\n")
    else:
        embed=discord.Embed(description="API key remove failed", color=0xFF0000)
        channel = client.get_channel(1006453355117281360)
        await channel.send(embed=embed)

@client.command()
async def apiadd(ctx, api):
    global waiting
    waiting = True
    response = requests.get("https://api.hypixel.net/key?key=" + api).json()
    if response['success'] == False:
        embed=discord.Embed(description="That API key seems to be invalid...", color=0xFF0000)
        await ctx.channel.send(embed=embed)
    else:
        with open("apikeys.txt", "a") as r:
            r.write(api + "\n")
        embed=discord.Embed(description="API key was added successfully!", color=0x00FF00)
        await ctx.channel.send(embed=embed)
    waiting = False

@client.command()
async def count(ctx, uuid):
    global waiting
    waiting = True
    if len(uuid) < 30:
        a = requests.get("https://playerdb.co/api/player/minecraft/" + uuid).json()
        uuid = (a['data']['player']['raw_id'])
    count = 0
    firstFound = False
    with open("db.txt", "r") as r:
        db = r.readlines()

    for i in db:
        if uuid in i:
            firstFound = True
            count += 1
        elif firstFound:
            break

    embed=discord.Embed(title=str(uuid + " exotics count"),description=str(count), color=0xFFC0CB)
    await ctx.channel.send(embed=embed)
    waiting = False

@client.command()
async def exotics(ctx, uuid):
    global waiting
    waiting = True
    if len(uuid) < 30:
        a = requests.get("https://playerdb.co/api/player/minecraft/" + uuid).json()
        uuid = (a['data']['player']['raw_id'])
    count = 0
    firstFound = False
    exotics = []
    with open("db.txt", "r") as r:
        db = r.readlines()

    for i in db:
        if uuid in i:
            firstFound = True
            count += 1
            exotics.append(str(i[i.find("|") + 1:i.find("|") + 7]) + " " + i[:i.find("|")])
            hexes = "0x" + str(i[i.find("|") + 1:i.find("|") + 7])
        elif firstFound:
            break

    desc = ""
    for i in exotics:
        desc += (i+"\n")
    if len(desc) >= 4096:
        desc = desc[:4082]
        desc = desc[:desc.rfind("\n")]
        desc += "\netc..."
    if len(desc) == 0:
        hexes = "0xFF0000"
    embed=discord.Embed(title=str(uuid + " has **" + str(count) + "** exotic(s)"),description=desc, color=int(hexes,16))
    await ctx.channel.send(embed=embed)
    waiting = False

@client.command()
async def skip(ctx, uuid):
    global waiting
    waiting = True
    if len(uuid) < 30:
        a = requests.get("https://playerdb.co/api/player/minecraft/" + uuid).json()
        uuid = (a['data']['player']['raw_id'])
    with open("skip.txt", "a") as a:
        a.write(uuid + "\n")
    embed=discord.Embed(description=uuid + " will be skipped from now on!", color=0xFF0000)
    try:
        await ctx.channel.send(embed=embed)
    except:
        print()
    waiting = False

@client.command()
async def mode(ctx, switch):
    global mods
    
    if switch.lower() == "high":
        mods == "high"
    elif switch.lower() == "all":
        mods = "all"
    else:
        embed=discord.Embed(description="Invalid mode. Available modes:\n   High\n   All", color=0xFF0000)
        try:
            await ctx.channel.send(embed=embed)
        except:
            print()

@tasks.loop()    
async def notifier():
    global stopa
    stopa = False
    global mods

    rare = ["Leaflet Chestplate","Leaflet Leggings","Leaflet Boots","Fairy Leggings","Fairy Chestplate","Fairy Boots","Crystal Boots","Crystal Leggings","Crystal Chestplate","Chestplate of The Pack","Blaze Chestplate","Blaze Leggings","Blaze Boots","Sponge Boots","Sponge Leggings","Sponge Chestplate","Tarantula Helmet","Tarantula Leggings","Bat Person Chestplate","Bat Person Leggings","Bat Person Boots","Pumpkin Helmet","Pumpkin Chestplate","Pumpkin Leggings","Pumpkin Boots","Cactus Helmet","Cactus Chestplate","Cactus Leggings","Cactus Boots","Growth Helmet","Growth Chestplate","Growth Leggings","Growth Boots","Cheap Tuxedo Boots","Cheap Tuxedo Leggings","Cheap Tuxedo Chestplate","Farm Suit"]
    count = 0
    knownExotics = []
    with open("apiKeys.txt", "r") as r:
        apis =  r.readlines()
    with open("armorNames.txt", "r") as r:
        armorNames =  r.readlines()
    with open("db.txt", "r") as r:
        db =  r.readlines()
    with open("skip.txt", "r") as r:
        skip =  r.readlines()

    skips = []
    for i in skip:
        skips.append(i.strip())
    start = time.time()
    for i in range(len(db)):
        if i == 0:
            with open("skip.txt", "r") as r:
                skip =  r.readlines()

            skips = []
            for i in skip:
                skips.append(i.strip())
        if stopa:
            return 0
        try:
            if i % 100 == 0:
                channel = client.get_channel(1006407222479298650)
                end = time.time()
                embed=discord.Embed(title="Logs", description=str("The last 100 igns took " + str(end-start) + " seconds."), color=0xFF5733)
                try:
                    await channel.send(embed=embed)
                except:
                    embed=discord.Embed(description="Error: (logs) " + str(e), color=0xFF0000)
                    channel = client.get_channel(1006453355117281360)
                    try:
                        await channel.send(embed=embed)
                    except:
                        print()
                print(str("The last 100 igns took " + str(end-start) + " seconds."))
                start = time.time()
            if count % 30 == 0:
                with open("apiKeys.txt", "r") as r:
                    apis = r.readlines()
            desc = ""
            exotics = ""
            uuid = db[i][db[i].find(",") + 1:db[i].find(",") + 33]
            i += 1
            if uuid in skips:
                continue
            nextUuid = db[i][db[i].find(",") + 1:db[i].find(",") + 33]
            i -= 1
            itemID = db[i][:db[i].find("|")]
            profileID = db[i][db[i].find("*") + 1:db[i].find(":")]
            currentHex = str(db[i][(db[i].find("|") + 1):(db[i].find("|") + 7)])
            itemName = itemID
            for i in armorNames:
                if itemID in i:
                    itemName = i[i.find(" ") + 1:].strip()
            if uuid == nextUuid:
                knownExotics.append(str("#" + str(currentHex) + " " + str(itemName)))
                continue
            else:
                knownExotics.append(str("#" + str(currentHex) + " " + str(itemName)))
            if mods == "high":
                for i in range(len(knownExotics)):
                    if knownExotics[i][knownExotics[i].find(" ") + 1:] in rare:
                        continue
                    else:
                        for j in range(len(knownExotics)):
                            total = sum(1 for x in knownExotics if knownExotics[i][knownExotics[i].find(" ") + 1:] in x)
                            if total >= 3:
                                continue
                            else:
                                print("Deleted element")
                                del knownExotics[i]
            if len(knownExotics) == 0:
                continue
            activeAPI = apis[count % len(apis)]
            hypixelResponse = requests.get("https://api.hypixel.net/status?uuid=" + uuid + "&key=" + activeAPI.strip()).json()
            try:
                if hypixelResponse['throttle']:
                    while True:
                        hypixelResponse = requests.get("https://api.hypixel.net/status?uuid=" + uuid + "&key=" + activeAPI.strip()).json()
                        await asyncio.sleep(0.5)
                        try:
                            hypixelResponse['throttle']
                        except:
                            break
                elif hypixelResponse['cause'] == "Invalid API key":
                    apir(activeAPI.strip())
                    apis.remove(activeAPI)
                    embed=discord.Embed(description="API key removed (invalid) - " + activeAPI.strip(), color=0xFF0000)
                    channel = client.get_channel(1006453355117281360)
                    try:
                        await channel.send(embed=embed)
                    except:
                        print()
            except:
                print(str(hypixelResponse))
            if hypixelResponse['session']['online']:
                try:
                    game = hypixelResponse['session']['gameType']
                except:
                    print("no game type")

                try:
                    game += str(" | " + hypixelResponse['session']['mode'])
                except:
                    print("no game mode")
                lapis = 0
                sup = 0
                young = 0
                for i in knownExotics:
                    d = i[i.find(" ") + 1:]
                    if d.strip() in rare:
                        desc += "<@&1006371448090284042>"
                    elif "Lapis" in i:
                        lapis += 1
                    elif "Superior" in i:
                        sup += 1
                    elif "Young" in i:
                        young += 1
                    exotics += str(i + "\n")

                if lapis > 2:
                    desc += "<@&1006371368255881317>"
                if sup > 0:
                    desc += "<@&1006371335095722045>"
                if young > 2:
                    desc += "<@&1006371281735790602>"
                if len(exotics) >= 1024:
                    exotics = exotics[:1016]
                    exotics = exotics[:exotics.rfind("\n")]
                    exotics += "\netc..."
                a = requests.get("https://playerdb.co/api/player/minecraft/" + uuid).json()
                username = (a['data']['player']['username'])
                colors = "0x" + str(knownExotics[0][1:7])
                embed=discord.Embed(title=str(username), url=str("https://sky.shiiyu.moe/stats/" + uuid + "/" + profileID), color=int(colors,16))
                embed.set_footer(text="This bot is still in development. Please DM stepsisters#9442 with any issues.")
                embed.add_field(name="UUID", value=str(uuid), inline=False)
                embed.add_field(name="Exotics", value=exotics, inline=True)
                embed.add_field(name="Gamemode", value=game, inline=True)
                channel = client.get_channel(1006371252077858856)
                if len(desc) > 0:
                    try:
                        await channel.send(desc)
                    except:
                        print()
                try:
                    await channel.send(embed=embed)
                except:
                    print()
            knownExotics = []
            count += 1
        except Exception as e:
            if "dfgsdfgs" in str(e):
                print("log error")
            else:
                embed=discord.Embed(description="Error: " + str(e), color=0xFF0000)
                channel = client.get_channel(1006453355117281360)
                try:
                    await channel.send(embed=embed)
                except:
                    print()
    if i == len(db) - 1:
        i = 0

client.run('MTAwNjIzNDg4MTYwNjU1Nzc2Nw.GA1h-e.sBazl5b2mhH07QU6CN_xgjbnWDtcIUhoJRMuag')