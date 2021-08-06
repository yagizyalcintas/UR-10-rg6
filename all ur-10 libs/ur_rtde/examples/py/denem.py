import json

with open("TM.json", "r") as f:
    tm_dict = json.load(f)

with open("config.json", "r") as f:
    config = json.load(f)

tm_string = json.dumps(tm_dict)
config_string = json.dumps(config)

keyList = []

for (key,value) in config.items():
    key_str = key
    key_str = "{{" + key_str + "}}"
    keyList.append(key_str)
   
    print(key_str)
#print(config)
#print(keyList)


dictionary_items = config.items()
sorted_items = sorted(dictionary_items)

for i in range(len(sorted_items)):
     sorted_items[i]

di = dict(sorted_items)
print(sorted_items)

# for key, value in config.items():
#     #tm_string = tm_string.replace("{{HTTP_IP_ADDRESS}}", "2222222")
#     tm_string = tm_string.replace('"{}"'.format(key), str(value)) #backslah bak
#     tm_string = tm_string.replace(key, str(value))


tm_modified_dict = json.loads(tm_string)
#print(tm_modified_dict)