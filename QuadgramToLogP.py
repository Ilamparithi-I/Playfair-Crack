import math
import json

with open('war and peace quadgrams.txt', 'r') as file:
    lines = file.readlines()

result = {}
total = 0

for line in lines:
    parts = line.strip().split()
    number = int(parts[1])
    total = total + number
    result[parts[0]] = number

for list in result:
    result[list] = math.log10(float(result[list])/float(total))

result["FLOOR"] = math.log10((0.01/float(total)))

with open('data.json', 'w') as json_file:
    json.dump(result, json_file)

