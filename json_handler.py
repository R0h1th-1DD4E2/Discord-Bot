import json 
from datetime import datetime, timedelta

def dump_json(response):
    data = {
        "access_time": datetime.now().strftime("%H:%M:%S"),
        "expire_date": (datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S") 
    }

    data.update(response) 

    with open("response.json", "w") as jsonfile:
        json.dump(data, jsonfile)
        jsonfile.close()

def load_json():
    with open("response.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        return data["access_time"] , data["expire_date"] , data["access_token"] , data["refresh_token"]