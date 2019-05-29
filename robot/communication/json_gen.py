import json

def generate_json(keys, values):
    x = {
            "type" : "status",
            "message" : {
                "status" : "online"
                }
        }
    
    for i in range(len(keys)):
        x["message"][keys[i]] = values[i]
        
    return json.dumps(x)
