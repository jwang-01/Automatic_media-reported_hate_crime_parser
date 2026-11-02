import json
with open("themessss.json", "r") as f:
    themes = json.load(f)

new = ["%"+x.split()[0]+"%" for x in themes] #just keeping the main parts





with open("themessss_new.json", "w") as f:
    f.write(json.dumps(new, indent=4))



