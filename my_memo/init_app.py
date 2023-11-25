import json

setting_info = {"opacity": 100,
                "backgourd": {
                    "color": "grey",
                    "rgb": (243, 242, 241),
                    "index": 5
                }}

with open("setting_info.json", "w") as json_file:
    json.dump(setting_info, json_file, indent=4)
