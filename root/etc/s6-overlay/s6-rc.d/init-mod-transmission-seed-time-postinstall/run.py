import json

transmission_settings = json.load(open("/config/settings.json"))
transmission_settings["idle-seeding-limit-enabled"] = False
json.dump(transmission_settings, open("/config/settings.json", "w"), indent=2)
