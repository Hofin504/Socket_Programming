import json

def readinfo_json(key) :  
    f = open("Data.json")
    x = json.loads(f.read())
    f.close()
    return x[key]