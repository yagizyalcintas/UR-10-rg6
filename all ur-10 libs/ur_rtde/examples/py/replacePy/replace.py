import json

with open("TM.json", "r") as f:
    tm_dict = json.load(f)

with open("config.json", "r") as f:
    config = json.load(f)

tm_string = json.dumps(tm_dict)

tm_string = tm_string.replace("<<", "")
tm_string = tm_string.replace(">>", "")

for key, value in config.items():
    #tm_string = tm_string.replace("{{HTTP_IP_ADDRESS}}", "2222222")
    tm_string = tm_string.replace('"{}"'.format(key), str(value))
    tm_string = tm_string.replace(key, str(value))


tm_modified_dict = json.loads(tm_string)
print(tm_modified_dict)