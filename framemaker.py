import sys


class File:
	CATEGORY_SPLITTER = "0"

	def __init__(self, filepath: str):
		self.file = filepath.replace("\\", "/").split("/")[-1]
		self.category = self.file.split(self.CATEGORY_SPLITTER)[0]


files = sorted([File(x) for x in sys.argv[1:] if x.lower().endswith(".tga")], key = lambda k: k.file)
if not files:
	input("ERROR: NO TGA FILES PROVIDED\nPress [enter] to quit.")
	exit()

categories = dict()
for f in files:
	if f.category not in categories:
		categories[f.category] = list()
	categories[f.category].append(f.file)
seq = 0
output = list()
for v in categories.values():
	seq += 1
	output.append(f"sequence {seq}\nloop")
	for path in v:
		output.append(f"frame {path} 1")
	output.append("")
output_dir = input("ENTER NAME OF TARGET DIRECTORY:\t").rstrip(".mks")
with open(f"{output_dir}.mks", "w") as fl:
	fl.write("\n".join(output))
input(f"{output_dir}.mks created\nPress [enter] to quit.")
