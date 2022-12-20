from discord.ext import commands
from config import MONGO_DB, GUILD, NG_API
from pymongo import MongoClient
import requests

client = MongoClient(MONGO_DB)
DBs = client.list_database_names
DB = client.DataBase
data = DB.data

class initialisation(commands.Cog):
    def __init__(self):
        if data.count_documents({}) == 0:
            get = requests.get(f'https://api.ngmc.co/v1/guilds/{GUILD.replace(" ","%20")}?expand=true&withStats=true', headers={'Authorization': NG_API}).json()
            try:
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

                init = {
                    "id": get['id'],
                    "checklist": checklist,
                    "log":log_members
                }
                data.insert_one(init)
                print("Initialisation completed!")
            except Exception as e:
                print("There was an issue with initialisation. Please insure that the guild name is correct.")