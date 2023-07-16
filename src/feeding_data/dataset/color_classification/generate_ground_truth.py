import os
import csv


header = ["file_name", "color", "shape", "box"]
colors = ["Red", "Green", "Blue"]

csvfile = open('objects_colors_dataset.csv', 'a', newline='')
writer = csv.writer(csvfile)
writer.writerow(header)

files = os.listdir(os.path.join("."))

for f in files:
    if "," in f:
        print("FAILIER AT FILE: {}".format(f))
        break
    if f.endswith(".jpg"):
        color = [x for x in colors if x in f]
        l = [f, color[0], "Cube", colors.index(color[0]) + 1]
        writer.writerow(l)
