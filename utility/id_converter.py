import json
import sys

def process_first_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        entries = data.get('entries', {})
        name_mapping = {}
        for entry_id, entry_value in entries.items():
            entry_name = entry_value.get('name', '')
            name_mapping[entry_name] = entry_id
            pages = entry_value.get('pages', {})
            for page_id, page_value in pages.items():
                page_name = page_value.get('name', '')
                name_mapping[page_name] = page_id
        return name_mapping

def process_second_json(file_path):
    with open(file_path, 'r') as file:
        json_objects = file.read().splitlines()
        name_mapping = {}
        for json_obj in json_objects:
            obj = json.loads(json_obj)
            name = obj.get('name', '')
            _id = obj.get('_id', '')
            pages = obj.get('pages', [])
            for page in pages:
                page_name = page.get('name', '')
                page_id = page.get('_id', '')
                name_mapping[page_name] = f"JournalEntry.{_id}"
                if page_id:
                    name_mapping[page_name] += f".JournalEntryPage.{page_id}"
        return name_mapping

def generate_third_dict(first_dict, second_dict):
    third_dict = {}
    for key, value in first_dict.items():
        if value in second_dict:
            third_dict[key] = second_dict[value]
    return third_dict

def save_as_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

# 处理第一个 JSON 文件
first_file_path = sys.argv[1]
first_dict = process_first_json(first_file_path)

# 处理第二个 JSON 文件
second_file_path = sys.argv[2]
second_dict = process_second_json(second_file_path)

# 生成第三个字典
third_dict = generate_third_dict(first_dict, second_dict)

# 保存第三个字典为 JSON 文件
output_file_path = sys.argv[3]
save_as_json(output_file_path, third_dict)
