import json
import os
import csv
from typing import Any

data_folder = os.path.join(".", "data")
json_file_path = os.path.join(data_folder, "sensors.json")
csv_file_path = os.path.join(data_folder, "sensors.csv")

with open(json_file_path, "r") as file:
    sensors: dict[str, dict[str, dict[str, Any]]] = json.load(file)

with open(
    csv_file_path,
    "w",
    newline="",
) as csv_file:
    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)

    # Base Header
    csv_writer.writerow(
        [
            "Vendor",
            "Camera",
            "Sensor Dimensions Name",
            "Focal Length",
            "Resolution Width",
            "Resolution Height",
            "Sensor mm Width",
            "Sensor mm Height",
            "Sensor mm Diagonal",
            "Sensor Inches Width",
            "Sensor Inches Height",
            "Sensor Inches Diagonal",
            "Info",
        ]
    )

    # Iterate through the JSON data to generate csv info
    for vendor, cameras in sensors.items():
        for camera, data in cameras.items():
            for dim_type, dim_data in data["sensor dimensions"].items():
                csv_writer.writerow(
                    [
                        vendor,
                        camera,
                        dim_type,
                        dim_data["focal length"],
                        dim_data["resolution"]["width"],
                        dim_data["resolution"]["height"],
                        dim_data["mm"]["width"],
                        dim_data["mm"]["height"],
                        dim_data["mm"]["diagonal"],
                        dim_data["inches"]["width"],
                        dim_data["inches"]["height"],
                        dim_data["inches"]["diagonal"],
                        data["info"].get("Other", ""),
                    ]
                )
