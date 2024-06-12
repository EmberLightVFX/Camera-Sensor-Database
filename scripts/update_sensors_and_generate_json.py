import math
import os
import re
import sys
import json

DEBUG = False
# Read input from stdin (provided via shell script)
if DEBUG:
    from pprint import pprint

    BODY = """"""

else:
    BODY = sys.argv[1]

data_folder = os.path.join(".", "data")
json_file_path = os.path.join(data_folder, "sensors.json")


def cleanup_block(text: str) -> tuple[str, str | None]:
    lines = text.splitlines()
    category = str(lines[0].strip())
    data = None
    if str(lines[2].strip()) != "_No response_":
        data = "\n".join(lines[2:]).strip()
    return (category, data)


# Function to extract and convert the first number to a numeric type
def extract_single_number(text: str) -> float:
    number: list[str] = re.findall(r"\d*\.\d+|\d+", text.replace(",", "."))
    return float(number[0]) if "." in number else int(number[0])


def extract_dual_numbers(text: str) -> list[float]:
    numbers = re.findall(r"\d*\.\d+|\d+", text.replace(",", "."))
    if any("." in value for value in numbers):
        return [float(num) for num in numbers[:2]]
    else:
        return [int(num) for num in numbers]


# Read existing sensors.json file if it exists
try:
    with open(json_file_path, "r") as f:
        sensors_data = json.load(f)
except FileNotFoundError:
    sensors_data = {}

vendor = None
camera = None

blocks = BODY.strip().split("### Name", 1)

## Camera info
camera_info = blocks[0].strip().split("### ")

# Vendor
category, data = cleanup_block(camera_info[2])
if data == "Other":
    category, data = cleanup_block(camera_info[3])
vendor = data
if vendor not in sensors_data:
    sensors_data[vendor] = {}

# Camera
category, data = cleanup_block(camera_info[4])
camera = data
if camera not in sensors_data[vendor]:
    sensors_data[vendor][camera] = {}

# Additional Information
category, data = cleanup_block(camera_info[5])
sensors_data[vendor][camera]["info"] = {}
if data:
    sensors_data[vendor][camera]["info"]["Other"] = data

# Auto-generate sensor dimensions
auto_sensor_size = "[X]" in camera_info[6]

# Sensor Dimensions
if "sensor dimensions" not in sensors_data[vendor][camera]:
    sensors_data[vendor][camera]["sensor dimensions"] = {}

## All resolution types
full_pixel_width = None
full_pixel_height = None
full_sensor_mm_width = None
full_sensor_mm_height = None
full_sensor_inches_width = None
full_sensor_inches_height = None
for block in blocks[1].split("### Name"):
    mm = None
    inches = None
    width = 0
    height = 0
    # Add back the name category that got removed from the split
    block = f"### Name{block}"

    dim_type = block.strip().split("### ")

    # Name
    category, data = cleanup_block(dim_type[1])
    if data is None:
        continue
    dim_name = data
    sensors_data[vendor][camera]["sensor dimensions"][dim_name] = {}

    # Focal Length
    category, data = cleanup_block(dim_type[2])
    if data:
        sensors_data[vendor][camera]["sensor dimensions"][dim_name]["focal length"] = (
            extract_single_number(data)
        )
    else:
        sensors_data[vendor][camera]["sensor dimensions"][dim_name]["focal length"] = ""

    # Resolution
    category, data = cleanup_block(dim_type[3])
    if data:
        res = extract_dual_numbers(data)
        sensors_data[vendor][camera]["sensor dimensions"][dim_name]["resolution"] = {
            "width": res[0],
            "height": res[1],
        }
        width = res[0]
        height = res[1]
        if auto_sensor_size and not full_pixel_width and not full_pixel_height:
            full_pixel_width = res[0]
            full_pixel_height = res[1]
    else:
        sensors_data[vendor][camera]["sensor dimensions"][dim_name]["resolution"] = {
            "width": "",
            "height": "",
        }

    # Sensor Size (mm)
    category, data = cleanup_block(dim_type[4])
    if data:
        mm = extract_dual_numbers(data)

    # Sensor Size (inches)
    category, data = cleanup_block(dim_type[5])
    if data:
        inches = extract_dual_numbers(data)

    if not mm and not inches:
        # If not the first dimension
        if auto_sensor_size:
            if (
                full_sensor_mm_width
                and full_sensor_mm_height
                and full_pixel_width
                and full_pixel_height
            ):
                mm = [
                    (width / full_pixel_width) * full_sensor_mm_width,
                    (height / full_pixel_height) * full_sensor_mm_height,
                ]
            if (
                full_sensor_inches_width
                and full_sensor_inches_height
                and full_pixel_width
                and full_pixel_height
            ):
                inches = [
                    (width / full_pixel_width) * full_sensor_inches_width,
                    (height / full_pixel_height) * full_sensor_inches_height,
                ]
        if not mm or not inches:
            raise AttributeError("You need at least one sensor size")
    elif mm and not inches:
        inches = [mm[0] / 25.4, mm[1] / 25.4]
    elif not mm:
        mm = [inches[0] * 25.4, inches[1] * 25.4]

    if auto_sensor_size:
        if inches and not full_sensor_inches_width and not full_sensor_inches_height:
            full_sensor_inches_width = inches[0]
            full_sensor_inches_height = inches[1]
        if mm and not (full_sensor_mm_width or full_sensor_mm_height):
            full_sensor_mm_width = mm[0]
            full_sensor_mm_height = mm[1]

    mm[0] = round(mm[0], 3)
    mm[1] = round(mm[1], 3)
    inches[0] = round(inches[0], 3)
    inches[1] = round(inches[1], 3)

    sensors_data[vendor][camera]["sensor dimensions"][dim_name]["mm"] = {
        "width": mm[0],
        "height": mm[1],
        "diagonal": round(math.sqrt(mm[0] ** 2 + mm[1] ** 2), 3),
    }
    sensors_data[vendor][camera]["sensor dimensions"][dim_name]["inches"] = {
        "width": inches[0],
        "height": inches[1],
        "diagonal": round(math.sqrt(inches[0] ** 2 + inches[1] ** 2), 3),
    }


# Write the updated dictionary back to sensors.json
if DEBUG:
    pprint(sensors_data)
else:
    with open(json_file_path, "w") as f:
        json.dump(sensors_data, f, indent=2)
