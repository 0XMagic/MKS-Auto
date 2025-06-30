import os
import sys
import json
import pathlib
import subprocess
import shutil


class File:
	CATEGORY_SPLITTER = "-"

	def __init__(self, filepath: str):
		self.fullpath = filepath.replace("\\", "/")
		self.file = filepath.replace("\\", "/").split("/")[-1]
		self.category = self.file.split(self.CATEGORY_SPLITTER)[0] if self.CATEGORY_SPLITTER in self.file else ""


files = sorted([File(x) for x in sys.argv[1:] if x.lower().endswith(".tga")], key = lambda k: k.file)
if not files:
	print("[ERROR] NO TGA FILES PROVIDED")
	os.system("pause")
	exit()

categories = dict()
for f in files:
	if f.category not in categories:
		categories[f.category] = list()
	categories[f.category].append(f.fullpath)
seq = 0
output = list()
for v in categories.values():
	seq += 1
	output.append(f"sequence {seq}\nloop")
	for path in v:
		output.append(f"frame {path} 1")
	output.append("")
output_name = ""
while not output_name:
	output_name = input("ENTER NAME OF MATERIAL:\t").lower()
	if not output_name or any(x in output_name for x in "<>:\"/\\|?*") or not output_name.isascii():
		print("Invalid name!")
		output_name = ""

output_dir = f"{output_name}.mks"
output_sht = f"{output_name}.sht"
output_tga = f"{output_name}.tga"

with open(output_dir, "w") as fl:
	fl.write("\n".join(output))

with open("config.json", "r") as fl:
	_json = json.load(fl)
	steam_dir = pathlib.Path(_json["SteamDir"])

if not steam_dir.is_dir():
	print("[ERROR] Steam is not found! Check config.json.")
	os.system("pause")
	exit()

mks_dir = steam_dir / "common/Team Fortress 2/bin/mksheet.exe"

if not mks_dir.is_file():
	print("[ERROR] Team Fortress 2 is not installed on this device!")
	os.system("pause")
	exit()

subprocess.call(str(mks_dir) + " " + output_dir)

vtex_dir = steam_dir / "common/Team Fortress 2/bin/vtex.exe"
tf_dir = steam_dir / "common/Team Fortress 2/"

copy_dir = tf_dir / "tf/materialsrc" / output_name

if not copy_dir.is_dir():
	copy_dir.mkdir(parents = True)

check_dir = copy_dir / output_dir
check_sht = copy_dir / output_sht
check_tga = copy_dir / output_tga

if check_dir.is_file():
	os.remove(check_dir)
if check_sht.is_file():
	os.remove(check_sht)
if check_tga.is_file():
	os.remove(check_tga)

shutil.move(output_dir, copy_dir)
shutil.move(output_sht, copy_dir)
shutil.move(output_tga, copy_dir)

output_sht = f"{copy_dir}/{output_sht}"

subprocess.Popen(str(vtex_dir) + f" -game \"{str(tf_dir / 'tf')}\" \"" + output_sht + "\"")
