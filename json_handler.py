import json 
from datetime import datetime, timedelta

dictionary = {
    "accessed_time": datetime.now().strftime("%H:%M:%S"),
    "expire_date": (datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S") 
}

response = {
    
}

dictionary.update(response)
    
with open("response.json", "w") as jsonfile:
    json.dump(dictionary, jsonfile)
    jsonfile.close()


with open("response.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print(data["expire_date"] > data["accessed_time"])
    jsonfile.close()