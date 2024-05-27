from collections import defaultdict
import math
import os
from pprint import pprint
import re
import json

DEBUG = False
VENDOR = ""
CAMERA = ""
BODY = """



"""


def process_line(line: str, mode: str | None) -> None | list[str | int | float]:
    pat_all = re.compile(
        r"(\d+)\s*[×x]\s*(\d+)\s+(.+?)\s+([\d.]+)\s*mm\s*[×x]\s*([\d.]+)\s*mm\s*\(([\d.]+)\s*in\s*x\s*([\d.]+)\s*in\)"
    )
    pat_mm = re.compile(
        r"(\d+)\s*[×x]\s*(\d+)\s+(.+?)\s+([\d.]+)\s*mm\s*[×x]\s*([\d.]+)\s*mm"
    )
    pat_sensor = re.compile(
        r"([\d.]+)\s*mm\s*[×x]\s*([\d.]+)\s*mm\s*\(([\d.]+)\s*in\s*x\s*([\d.]+)\s*in\)"
    )

    descriptor = "All"
    res_x = ""
    res_y = ""
    mm_x = None
    mm_y = None
    inch_x = None
    inch_y = None
    if match := pat_all.match(line):
        descriptor = match[3].strip()
        res_x = int(match[1])
        res_y = int(match[2])
        mm_x = round(float(match[4]), 3)
        mm_y = round(float(match[5]), 3)
        inch_x = round(float(match[6]), 3)
        inch_y = round(float(match[7]), 3)
    elif match := pat_mm.match(line):
        descriptor = match[3].strip()
        res_x = int(match[1])
        res_y = int(match[2])
        mm_x = round(float(match[4]), 3)
        mm_y = round(float(match[5]), 3)
        inch_x = round(float(match[4]) / 25.4, 3)
        inch_y = round(float(match[5]) / 25.4, 3)
    elif match := pat_sensor.match(line):
        mm_x = round(float(match[1]), 3)
        mm_y = round(float(match[2]), 3)
        inch_x = round(float(match[3]), 3)
        inch_y = round(float(match[4]), 3)
    else:
        return None

    if mode:
        descriptor = f"{mode} {descriptor}"

    return [descriptor, res_x, res_y, mm_x, mm_y, inch_x, inch_y]


data_folder = os.path.join(".", "data")
json_file_path = os.path.join(data_folder, "sensors.json")
# Read existing sensors.json file if it exists
if not DEBUG:
    try:
        with open(json_file_path, "r") as f:
            sensors_data = json.load(f)
    except FileNotFoundError:
        sensors_data = {}
else:
    sensors_data = {}

# Vendor
vendor = VENDOR
if vendor not in sensors_data:
    sensors_data[vendor] = {}

# Camera
camera = CAMERA
if camera not in sensors_data[vendor]:
    sensors_data[vendor][camera] = {}

# Additional Information
sensors_data[vendor][camera]["info"] = {}

# Sensor Dimensions
if "sensor dimensions" not in sensors_data[vendor][camera]:
    sensors_data[vendor][camera]["sensor dimensions"] = {}

# Process the data

# Process each line, maintaining the current mode
lines = BODY.strip().split("\n")

mode = None
results = []
for line in lines:
    if line.strip().endswith("Mode"):
        mode = line.strip()
    elif processed := process_line(line, mode):
        results.append(processed)
    else:
        mode = None


# Group by descriptors to count their occurrences
descriptor_count = defaultdict(int)
for item in results:
    descriptor_count[item[0]] += 1

# Prepare the final results
final_results: list[list[str | int | float]] = []
for item in results:
    descriptor, res1, res2, mm1, mm2, in1, in2 = item
    if descriptor_count[descriptor] > 1:
        descriptor_with_resolution = f"{descriptor} {res1} x {res2}"
    else:
        descriptor_with_resolution = descriptor
    final_results.append([descriptor_with_resolution, res1, res2, mm1, mm2, in1, in2])

for data in final_results:
    # Dimension name + focal length
    sensors_data[vendor][camera]["sensor dimensions"][data[0]] = {
        "focal length": "",
        "resolution": {"width": data[1], "height": data[2]},
        "mm": {
            "width": data[3],
            "height": data[4],
            "diagonal": round(math.sqrt(data[3] ** 2 + data[4] ** 2), 3),
        },
        "inches": {
            "width": data[5],
            "height": data[6],
            "diagonal": round(math.sqrt(data[5] ** 2 + data[6] ** 2), 3),
        },
    }

# Write the updated dictionary back to sensors.json
if DEBUG:
    pprint(sensors_data)
else:
    print(f"{vendor} - {camera}")
    with open(json_file_path, "w") as f:
        json.dump(sensors_data, f, indent=2)
