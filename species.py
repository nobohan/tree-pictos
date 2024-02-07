import csv
import shutil

prefix = ["B3", "B5", "B3+", "B4+", "B5+", "B3-", "B4-", "B5-", "C3", "C4", "C5"]
suffix = ["", "d1", "d2", "d3", "p", "d1p", "d2p", "d3p", "o", "d1o", "d2o", "d3o"]

with open("species-symbol-matrix.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    next(reader, None)
    i = 0
    for row in reader:
        j = 0
        for col in row:
            if i >= len(prefix):
                break
            if j > 0 and col and col != "/":
                species_name = col
                symbol_name = f"{prefix[i]}{suffix[j-1]}"
                if symbol_name in ["B3", "B3p", "B3o"]:  # special cases
                    if symbol_name == "B3":
                        symbol_name = "B"
                    else:
                        symbol_name = f"{symbol_name[0]}{symbol_name[2]}"

                print(species_name, symbol_name)
                shutil.copy(f"{symbol_name}.svg", f"species/{species_name}.svg")
            j = j + 1
        i = i + 1