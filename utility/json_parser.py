
import json

with open("zh-CN/swade-core-rules.swade-edges.json", "r",encoding="utf8") as f:
    data = json.load(f)
with open("swade-edges.json", "r", encoding="utf8") as src:
    src_data = json.load(src) 

#data = data["entries"]
#src_data = src_data["entries"]
#print(data['entries'])
#print(src_data['entries'])
if data['label'] == 'SWADE Rules':
    for entry in data['entries']:
        print(entry)
        for page in data['entries'][entry]['pages']:
            if page in src_data['entries']:
                data['entries'][entry]['pages'][page] = src_data['entries'][page]
                print(data['entries'][entry]['pages'][page])
else:
    for entry in data['entries']:
        #print(entry)
        if entry in src_data['entries']:
            for attr in src_data['entries'][entry]:
                #if attr in data['entries'][entry]:    
                data['entries'][entry][attr] = src_data['entries'][entry][attr]
                print(data['entries'][entry])
    #print(entry["biography"])
    #print(entry)
with open("swade-core-rules.swade-edges.json", "w", encoding="utf8") as dst:
    json.dump(data, dst, ensure_ascii=False) 