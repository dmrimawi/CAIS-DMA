import os
import csv
import re

def rename_jpg_files(directory):
  # loop over all files in the directory
  for file in os.listdir(directory):
    # check if the file has jpg extension
    if file.endswith(".jpg"):
      # get the file name without extension
      name = os.path.splitext(file)[0]
      # remove any special characters from the name using regular expression
      name = re.sub("[^a-zA-Z0-9]", "", name)
      # add the jpg extension back
      new_name = name + ".jpg"
      # rename the file using os.rename
      os.rename(os.path.join(directory, file), os.path.join(directory, new_name))

header = ["id", "file_name", "color", "shape", "box"]
colors = ["Red", "Green", "Blue"]

rename_jpg_files(os.path.join("."))

csvfile = open('objects_colors_dataset.csv', 'a', newline='')
writer = csv.writer(csvfile)
writer.writerow(header)

files = os.listdir(os.path.join("."))

counter = 1
for f in files:
    if "," in f:
        print("FAILIER AT FILE: {}".format(f))
        break
    if f.endswith(".jpg") and "Cube" in f:
        try:
            color = [x for x in colors if x in f]
            l = [counter, f, color[0], "Cube", colors.index(color[0]) + 1]
            writer.writerow(l)
            counter = counter + 1
        except Exception as exp:
            raise Exception("Failed at {}, got exception {}".format(f, str(exp)))
