import json
import os
from typing import Any
import yaml

data_folder = os.path.join(".", "data")
json_file_path = os.path.join(data_folder, "sensors.json")
yaml_file_path = os.path.join(data_folder, "sensors.yaml")

with open(json_file_path, "r") as file:
    sensors: dict[str, dict[str, dict[str, Any]]] = json.load(file)

with open(yaml_file_path, "w") as file:
    yaml.dump(sensors, file, sort_keys=False)
