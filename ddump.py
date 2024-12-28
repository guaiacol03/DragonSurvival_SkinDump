import base64
import itertools
import json
import os
import shutil
import sys
import requests
import argparse
SKINS_API = "https://api.github.com/repositories/280658566/git/trees/6597d654e16568d2d9e2cdf0dc372041cb081c35"
DUMP_PATH = ".dump"
STAGE_NAMES = ["newborn", "young", "adult"]
TYPE_NAMES = ["cave", "forest", "sea"]

parser = argparse.ArgumentParser(description="A tool to dump dragon skins from BlackAures repo")
subparsers = parser.add_subparsers(dest="command", required=True, help="Command to run")
subparsers.add_parser("list", help="List available skins")

dump_parser = subparsers.add_parser("dump", help="Dump skin to texture pack")
dump_parser.add_argument("name", type=str, help="Player name to dump")
dump_parser.add_argument("type", type=str, help="Dragon type to assign [forest,cave,sea]")

info_parser = subparsers.add_parser("info", help="Show info about player's skin")
info_parser.add_argument("name", type=str, help="Name to display info for")

dump_parser.add_argument('--key', type=str, help="The key argument", required=False)
args = parser.parse_args()

if args.key is not None:
    headers = {
        "Authorization": f"Bearer {args.key}",
        "Accept": "application/vnd.github+json"  # GitHub's recommended media type for API responses
    }
else:
    headers = None

res_list = requests.get(SKINS_API, headers=headers)
print("Fetching skin list from GitHub...")
if res_list.status_code != 200:
    msg = json.loads(res_list.content)["message"]
    raise Exception(f"HTTP Status Code: {res_list.status_code}. Message: {msg}")

def extract_player(filename):
    fn_spl = filename.split("_")
    fn_spl += fn_spl.pop(-1).split(".")
    fn_ind = next((i for i,v in enumerate(fn_spl) if v in STAGE_NAMES))
    return '_'.join(fn_spl[:fn_ind])

skin_list = res_list.json()['tree']
skin_dict = dict()
for k, v in itertools.groupby(skin_list, lambda obj: extract_player(obj['path'])):
    skin_dict[k] = list(v)

if hasattr(args, 'name'):
    if args.name not in skin_dict:
        print(f"Player {args.name} has no skin. Check 'list' for available")
        sys.exit(1)

if args.command == "list":
    print("{player name}: {texture count}")
    for k, v in skin_dict.items():
        print(f"{k}: {len(v)}")
elif args.command == "dump":
    if args.type not in TYPE_NAMES:
        raise Exception(f"Invalid skin type: {args.type}. Valid types are {TYPE_NAMES}")

    if os.path.exists(DUMP_PATH):
        print("Dump directory already exists. Removing")
        shutil.rmtree(DUMP_PATH)
    os.makedirs(DUMP_PATH)

    os.makedirs(DUMP_PATH + "/assets/dragonsurvival/textures/dragon/")
    pack_mcmeta = {
        "pack": {
            "pack_format": 6,
            "description": f"Dragon skin dumped from player {args.name}"
        }
    }
    with open(DUMP_PATH + "/pack.mcmeta", 'w') as file:
        json.dump(pack_mcmeta, file, indent=4)

    player = skin_dict[args.name]
    for v in player:
        v_url = v['url']
        print(f"Downloading {v_url}")
        res_skin = requests.get(v_url, headers=headers)
        if res_skin.status_code != 200:
            msg = json.loads(res_list.content)["message"]
            raise Exception(f"HTTP Status Code: {res_list.status_code}. Message: {msg}")
        res_skj = res_skin.json()

        skin_dec = base64.b64decode(res_skj['content'].replace("\n", ""))
        f_name = args.type + v['path'][len(args.name):]
        with open(DUMP_PATH + "/assets/dragonsurvival/textures/dragon/" + f_name, "wb") as file:
            file.write(skin_dec)

    print("Packing skins to a texture pack...")
    shutil.make_archive("dump-" + args.name, 'zip', DUMP_PATH)

elif args.command == "info":
    player = skin_dict[args.name]
    print(f"{args.name} has {len(player)} textures:")
    for v in player:
        print(f" - {v['path']}")
    print(1)