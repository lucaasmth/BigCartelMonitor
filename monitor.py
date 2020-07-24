import requests, configparser, json, time
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read("config.ini")

url = config["Config"]["webhook"]
shopname = config["Config"]["shopname"]
delay = int(config["Config"]["delay"])

old_items_list = []

old_items = requests.get("https://api.bigcartel.com/%s/products.json" % shopname).json()
for item in old_items:
	old_items_list.append(item["id"])

print("Stored already avaliable items")

while True:
	items_list = []

	print("Checking products...")
	items = requests.get("https://api.bigcartel.com/%s/products.json" % shopname).json()

	for item in items:
		items_list.append(item["id"])

	for item in items:
		if item["id"] not in old_items_list:
			data = {}
			data["username"] = (shopname + " Monitor")
			data["embeds"] = []
			embed = {}
			embed["title"] = "New item detected"
			embed["description"] = "Title : %s\nPrice : %s€" % (item["name"], item["options"][0]["price"])
			embed["url"] = "https://%s.bigcartel.com%s" % (shopname, item["url"])
			embed["color"] = 255
			image = {}
			image["url"] = item["images"][0]["url"]
			embed["image"] = image
			data["embeds"].append(embed)
			requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
			print("Found new item: %s" % item["name"])
			old_items_list.append(item["id"])

	time.sleep(delay)