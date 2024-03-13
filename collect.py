from pathlib import Path
from collections import defaultdict
import httpx

# TODO: Run ghtodep at the start of the script
# Using a manual data dump for now - Generated with pipx run ghtopdep https://github.com/iced-rs/iced --rows 50 --json
items = [
    {"url": "https://github.com/0x192/universal-android-debloater", "stars": 8649},
    {"url": "https://github.com/veloren/veloren", "stars": 3367},
    {"url": "https://github.com/GyulyVGC/sniffnet", "stars": 3317},
    {"url": "https://github.com/ajour/ajour", "stars": 1016},
    {"url": "https://github.com/mtkennerly/ludusavi", "stars": 902},
    {"url": "https://github.com/rust-rosetta/rust-rosetta", "stars": 674},
    {"url": "https://github.com/PolyMeilex/Neothesia", "stars": 558},
    {"url": "https://github.com/rnd-ash/OpenVehicleDiag", "stars": 557},
    {"url": "https://github.com/robbert-vdh/nih-plug", "stars": 526},
    {"url": "https://github.com/greatest-ape/OctaSine", "stars": 452},
    {"url": "https://github.com/Ciantic/VirtualDesktopAccessor", "stars": 433},
    {"url": "https://github.com/oknozor/onagre", "stars": 264},
    {"url": "https://github.com/ZakisM/bl3_save_edit", "stars": 209},
    {"url": "https://github.com/pop-os/cosmic-comp", "stars": 199},
    {"url": "https://github.com/iced-rs/iced_aw", "stars": 191},
    {"url": "https://github.com/veloren/Airshipper", "stars": 177},
    {"url": "https://github.com/iced-rs/iced_audio", "stars": 142},
    {"url": "https://github.com/pop-os/cosmic-applets", "stars": 126},
    {"url": "https://github.com/yamadapc/augmented-audio", "stars": 125},
    {"url": "https://github.com/wizardsardine/liana", "stars": 97},
    {"url": "https://github.com/Inspirateur/SimpleRenamer", "stars": 97},
    {"url": "https://github.com/WootingKb/wooting-analog-sdk", "stars": 82},
    {"url": "https://github.com/w3champions/flo", "stars": 76},
    {"url": "https://github.com/forcia/rustbook", "stars": 76},
    {"url": "https://github.com/pop-os/cosmic-settings", "stars": 69},
    {"url": "https://github.com/carl-anders/slimevr-wrangler", "stars": 64},
    {"url": "https://github.com/brianch/offline-chess-puzzles", "stars": 62},
    {"url": "https://github.com/Joylei/plotters-iced", "stars": 60},
    {"url": "https://github.com/gamebooster/soundboard", "stars": 57},
    {"url": "https://github.com/Tarnadas/smmdb-client", "stars": 53},
    {"url": "https://github.com/hugopeixoto/ptcg-detection", "stars": 47},
    {"url": "https://github.com/jazzfool/iced_video_player", "stars": 47},
    {"url": "https://github.com/tindleaj/miso", "stars": 45},
    {"url": "https://github.com/auyer/Protonup-rs", "stars": 43},
    {"url": "https://github.com/MQuy/mbrowser", "stars": 42},
    {"url": "https://github.com/linkage-rs/linkage", "stars": 42},
    {"url": "https://github.com/FuzzrNet/Fuzzr", "stars": 41},
    {"url": "https://github.com/EndlessSkyCommunity/ESLauncher2", "stars": 40},
    {"url": "https://github.com/Joylei/anim-rs", "stars": 39},
    {"url": "https://github.com/revault/revault-gui", "stars": 39},
    {"url": "https://github.com/10XGenomics/enclone", "stars": 38},
    {"url": "https://github.com/sergev/vak-opensource", "stars": 37},
    {"url": "https://github.com/pop-os/cosmic-text-editor", "stars": 35},
    {"url": "https://github.com/pop-os/cosmic-launcher", "stars": 34},
    {"url": "https://github.com/BKSalman/ytdlp-gui", "stars": 34},
    {"url": "https://github.com/aevyrie/tolstack", "stars": 34},
    {"url": "https://github.com/eorzeatools/microlaunch", "stars": 32},
    {"url": "https://github.com/DankBSD/waysmoke", "stars": 31},
    {"url": "https://github.com/ka1mari/elysium", "stars": 29},
    {"url": "https://github.com/tasgon/bevy_iced", "stars": 29},
    {"url": "https://github.com/waycrate/exwlshelleventloop", "stars": 3},
]

all_urls = [d["url"] for d in items]

readme_file = Path().cwd().joinpath("readme.md")
mkdown_text = readme_file.read_text(encoding="utf-8")

content_start = mkdown_text.find("<!-- CONTENT -->")
content_end = mkdown_text.find("<!-- END CONTENT -->")
content_lines = mkdown_text[content_start:content_end].splitlines()
precontent = mkdown_text[:content_start+len("<!-- CONTENT -->")+2]
postcontent = mkdown_text[content_end:]

proj_types = []
cur_lines_by_proj = defaultdict(list)
cur_type = None
for line in content_lines:
    if not line:
        continue
    if line.startswith("##"):
        _ = cur_lines_by_proj[cur_type]
        cur_type = line[3:]
        proj_types.append(cur_type)
    elif cur_type:
        cur_lines_by_proj[cur_type].append(line)


used_urls = [url for url in all_urls if url in mkdown_text]
unused_urls = [url for url in all_urls if url not in mkdown_text]

print(f"{len(unused_urls)} URLs remaining")

ITERATE = True  # Set to false for testing other things before the main loop
if ITERATE:
    completed = defaultdict(list)
    for url in unused_urls:
        proj_name = url.split("/")[-1]
        proj_owner = url.split("/")[-2]

        print("\n-----")
        print(f"{proj_name}: {url}")

        try:
            # Get project name
            while True:
                try:
                    print("Available Project Types:")
                    for i, proj_t in enumerate(proj_types):
                        print(f"\t[{i+1}]: {proj_t}")
                    proj_type_selection = int(input("Select: "))

                    proj_type = proj_types[proj_type_selection - 1]
                    break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt()
                except:
                    continue

            # Get Description
            description = input("Description: ")
            if description[-1] != ".":
                description += "."

            # Get iced version
            iced_version = input("Iced version used: ")

            print(f"Iced @{iced_version}")
            version_badge = f'<img style="vertical-align: sub; padding-right: 7px" src="https://img.shields.io/badge/{iced_version}-blue?logo=iced&style=plastic">'

            completed[proj_type].append(f"- {version_badge}[{proj_name}]({url}) - {description}")
            print("-----\n")
        except Exception as e:
            print("Exception: ", e)
            break
        except KeyboardInterrupt:
            break
    print("\n")

    # Combine existing list items with the ones we've just created
    for proj_type, list_items in cur_lines_by_proj.items():
        print(proj_type, list_items)
        completed[proj_type].extend(list_items)

    completed.pop(None)
    # Write content to file
    print(f"Adding {len(list_items)} new entries")
    new_content = ""
    for proj_type, list_items in completed.items():
        new_content += f"## {proj_type}\n\n"

        list_items.sort()
        new_content += "\n".join(list_items)
        new_content += "\n\n"
    print(new_content)

    readme_file.write_text(precontent + new_content + postcontent)
