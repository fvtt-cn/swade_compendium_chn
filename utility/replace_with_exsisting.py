import json
import os
import argparse

def process_json_file(src, dict):
    with open(dict, 'r') as dict_file:
        dict_data = json.load(dict_file)
        dict_entries = dict_data.get('entries', {})

    with open(src, "r", encoding="utf-8") as src_file:
        src_data = json.load(src_file)
        src_entries = src_data.get('entries', {})
        for entry_key, entry_value in src_entries.items():
            if entry_key in dict_entries:
                for item in dict_entries[entry_key]:
                    src_entries[entry_key][item] = dict_entries[entry_key][item]
    
    output_file_name = f"{os.path.splitext(src)[0]}_output.json"
    with open(output_file_name, "w", encoding="utf-8") as file:
        json.dump(src_data, file, indent=4, ensure_ascii=False)

    print(f"Output file '{output_file_name}' created.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON file.")
    parser.add_argument("src_file", help="src file")
    parser.add_argument("dict_file", help="dict JSON file")
    args = parser.parse_args()

    process_json_file(args.src_file, args.dict_file)