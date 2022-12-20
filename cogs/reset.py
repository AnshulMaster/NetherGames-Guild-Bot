from discord.ext import commands, tasks
from pymongo import MongoClient
from config import *
import requests
import schedule

client = MongoClient(MONGO_DB)
DBs = client.list_database_names
DB = client.DataBase
data = DB.data

def reset():

    data1 = data.find()[0]
    get = requests.get(f'https://api.ngmc.co/v1/guilds/{data1["id"]}?expand=true&withStats=true', headers={'Authorization': NG_API}).json()
    members = []
    log_members = []
    checklist = []
    members.append(get["leader"])
    log_members.append(get['leader']["name"])
    for i in get["officers"]:
        members.append(i)
        log_members.append(i["name"])
    for i in get["members"]:
        log_members.append(i["name"])
        members.append(i)
    for p in members:
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

        data.update_one({"id": get['id']}, {
            "$set":{"checklist":checklist},
        })

schedule.every().monday.at("00:00").do(reset)

class resert(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop.start()
    
    @tasks.loop(seconds=1)
    async def loop(self):
        schedule.run_pending()

async def setup(client):
    await client.add_cog(resert(client))