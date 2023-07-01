import json
import argparse
import os

def extract_actions(json_data):
    actions = json_data.get("system", {}).get("actions", {})
    extracted_actions = {}

    if "skill" in actions:
        extracted_actions["skill"] = actions["skill"]

    additional_actions = actions.get("additional", {})
    if additional_actions:
        extracted_actions["additional"] = {key: {"name": value["name"]} for key, value in additional_actions.items()}

    return extracted_actions

def extract_field(data, field):
    fields = field.split(".")
    for f in fields:
        if isinstance(data, dict) and f in data:
            data = data[f]
        else:
            return None
    return data

def process_json_file(file_name, mapping_file):
    with open(mapping_file, "r", encoding="utf-8") as mapping_file:
        mapping_data = json.load(mapping_file)

    mapping = mapping_data["mapping"]

    with open(file_name, "r", encoding="utf-8") as file:
        json_lines = file.readlines()

    output_data = {
        "label": os.path.basename(file_name),
        "mapping": mapping,
        "entries": {}
    }

    for line in json_lines:
        json_data = json.loads(line.strip())

        extracted_data = {}
        extracted_data["name"] = extract_field(json_data, "name")  # 提取"name"字段并添加到extracted_data中

        for key, value in mapping.items():
            field_data = extract_field(json_data, value)
            if field_data is not None:
                extracted_data[key] = field_data

        actions = extract_actions(json_data)
        if actions:
            extracted_data["actions"] = actions

        if "actions" not in extracted_data:
            extracted_data.pop("actions", None)

        output_data["entries"][json_data["name"]] = extracted_data

    output_file_name = f"output_{os.path.splitext(file_name)[0]}.json"
    with open(output_file_name, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

    print(f"Output file '{output_file_name}' created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON file.")
    parser.add_argument("file_name", help="JSON file to process")
    parser.add_argument("mapping_file", help="Mapping JSON file")
    args = parser.parse_args()

    process_json_file(args.file_name, args.mapping_file)
