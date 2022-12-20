from discord.ext import commands, tasks
from pymongo import MongoClient
from config import *
import requests

client = MongoClient(MONGO_DB)
DBs = client.list_database_names
DB = client.DataBase
data = DB.data

class update_log(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_log.start()

    @tasks.loop(minutes=15)
    async def update_log(self):
        data1 = data.find()[0]
        checklist = data1["checklist"]
        get = requests.get(f'https://api.ngmc.co/v1/guilds/{data1["id"]}?expand=true&withStats=true', headers={'Authorization': NG_API}).json()
        members_data = []
        members = []
        members_data.append(get["leader"])
        members.append(get['leader']["name"])
        for i in get["officers"]:
            members_data.append(i)
            members.append(i["name"])
        for i in get["members"]:
            members.append(i["name"])
            members_data.append(i)
        
        pre_data = []
        for m in checklist:
            pre_data.append(m["name"])

        for p in members:
            if not p in pre_data:
                data2 = {
                        "name": p["name"],
                        "cq": int(p["winsData"]["CQ"]),
                        "bw": int(p["winsData"]["BW"]),
                        "tb": int(p["winsData"]["TB"]),
                        "sw": int(p["winsData"]["SW"]),
                        "sg": int(p["winsData"]["SG"]),
                        "total": p["winsData"]["CQ"]+p["winsData"]["BW"]+p["winsData"]["TB"]+p["winsData"]["SW"]+p["winsData"]["SG"]
                    }
                checklist.append(data2)
                print(f"Player added: {p['name']}")

        new_log = []

        if LOG_CHANNEL:
            try:
                channel = self.client.get_channel(LOG_CHANNEL)

                for p in data1["log"]:
                    if p  not in members:
                        await channel.send(f"**{p}** Left the guild.")
                for p in members:
                    new_log.append(p)
                    if p not in data1["log"]:
                        await channel.send(f"**{p}** Joined the guild!")
            except Exception as e:
                print("Invalid Channel ID.")

        data.update_one({"id": get['id']}, {
            "$set":{"checklist":checklist},
            "$set":{"log":new_log}
        })

async def setup(client):
    await client.add_cog(update_log(client))