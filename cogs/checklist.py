from discord import *
from discord.ext import commands
from pymongo import MongoClient
from config import MONGO_DB, NG_API, REQUIREMENTS
import requests

client = MongoClient(MONGO_DB)
DBs = client.list_database_names
DB = client.DataBase
data = DB.data

def sorter(item):
    return item['total']

class checklist(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @app_commands.command(name="checklist", description="Shows the weekly checklist of the guild")
    @app_commands.describe(expand="Expands the checklist and shows more data of each player.")
    @app_commands.choices(expand=[
        app_commands.Choice(name="True", value=1),
        app_commands.Choice(name="False", value=2)
    ])
    async def checklist(self,interaction=Interaction, expand: app_commands.Choice[int]=None):
            await interaction.response.defer()
            data1 = data.find()[0]
            try:
                get = requests.get(f'https://api.ngmc.co/v1/guilds/{data1["id"]}?expand=true&withStats=true', headers={'Authorization': NG_API}).json()
                members = []
                final_data = []
                members.append(get["leader"])
                for i in get["officers"]:
                    members.append(i)
                for i in get["members"]:
                    members.append(i)

                data1 = data1["checklist"]

                for p in members:
                    for p2 in data1:
                        if p["name"] == p2["name"]:
                            data2 = {
                                "name": p["name"],
                                "cq": int(p["winsData"]["CQ"])-p2["cq"],
                                "bw": int(p["winsData"]["BW"])-p2["bw"],
                                "tb": int(p["winsData"]["TB"])-p2["tb"],
                                "sw": int(p["winsData"]["SW"])-p2["sw"],
                                "sg": int(p["winsData"]["SG"])-p2["sg"],
                                "total": p["winsData"]["CQ"]+p["winsData"]["BW"]+p["winsData"]["TB"]+p["winsData"]["SW"]+p["winsData"]["SG"]-p2["total"]
                            }
                            final_data.append(data2)
                            data1.remove(p2)

                final_data.sort(key=sorter, reverse=True)

                stats = ""
                fail = ""
                xp = 0
                num = 0
                bw = 0
                sw = 0
                tb = 0
                cq = 0
                sg = 0

                if not expand or expand.name == "False":
                    for p in final_data:
                        num += 1
                        total = p['total']
                        xp += total*10
                        if p['total'] < REQUIREMENTS:
                            d = f"\n `{p['name']}`: **{total}** Wins"
                            fail += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 1 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥇 `{p['name']}`: **{total}** Wins"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 2 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥈 `{p['name']}`: **{total}** Wins"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 3 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥉 `{p['name']}`: **{total}** Wins"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        else:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n{num}. `{p['name']}`: **{total}** Wins"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                else:
                    for p in final_data:
                        num += 1
                        total = p['total']
                        xp += total*10
                        if p['total'] < REQUIREMENTS:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥇 `{p['name']}`: {total} (BW: {p['bw']}, SW: {p['sw']}, TB: {p['tb']}, CQ: {p['cq']}, SG: {p['sg']})"
                            fail += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 1 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥇 `{p['name']}`: {total} (BW: {p['bw']}, SW: {p['sw']}, TB: {p['tb']}, CQ: {p['cq']}, SG: {p['sg']})"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 2 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥈 `{p['name']}`: {total} (BW: {p['bw']}, SW: {p['sw']}, TB: {p['tb']}, CQ: {p['cq']}, SG: {p['sg']})"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        elif num == 3 and p['total'] != 0:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n🥉 `{p['name']}`: {total} (BW: {p['bw']}, SW: {p['sw']}, TB: {p['tb']}, CQ: {p['cq']}, SG: {p['sg']})"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]
                        else:
                            total = p["bw"]+p["sw"]+p["tb"]+p["cq"]+p["sg"]
                            d = f"\n{num}. `{p['name']}`: {total} (BW: {p['bw']}, SW: {p['sw']}, TB: {p['tb']}, CQ: {p['cq']}, SG: {p['sg']})"
                            stats += d
                            bw += p["bw"]
                            sw += p["sw"]
                            tb += p["tb"]
                            cq += p["cq"]
                            sg += p["sg"]

                emb = Embed(title=f"__{get['name']}'s OverAll Statistics__", description=f"""
》Bedwars: {bw}
》Skywars: {sw}
》The Bridge: {tb}
》Conquest: {cq}
》Survival Games: {sg}
》XP: {xp}""")
                emb2 = Embed(
                    title="__Passed__", description=stats, color=0x1f8b4c)
                emb3 = Embed(
                    title="__Failed__", description=fail, color=0xc7201a)
                if stats=="":
                    await interaction.followup.send(embeds=[emb, emb3])
                else:
                    await interaction.followup.send(embeds=[emb, emb2, emb3])
            except Exception as e:
                await interaction.followup.send(e)

async def setup(client):
    await client.add_cog(checklist(client))