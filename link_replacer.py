import sys
import json
import os

def process_json_file(file_path, mappings):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    entries = data.get('entries', {})
    for entry_key, entry_value in entries.items():
        if 'pages' in entry_value:
            pages = entry_value['pages']
            for page_key, page_value in pages.items():
                if 'text' in page_value:
                    page_value['text'] = replace_text(page_value['text'], mappings)
        if 'items' in entry_value:
            items = entry_value['items']
            for items_key, items_value in items.items():
                if 'description' in items_value:
                    items_value['description'] = replace_text(items_value['description'], mappings)
        if 'description' in entry_value:
                    entry_value['description'] = replace_text(entry_value['description'], mappings)
        if 'biography' in entry_value:
                    entry_value['biography'] = replace_text(entry_value['biography'], mappings)
        if 'results' in entry_value:
            results = entry_value['results']
            for result_key, result_value in results.items():
                results[result_key] = replace_text(result_value, mappings)
    
    return data

def replace_text(text, mappings):
    for name, id_ in mappings.items():
        search_str = '@Compendium[swade-core-rules.swade-rules.{name}]'.format(name=name)
        replace_str = '@UUID[Compendium.swade-core-rules.swade-rules.{id}]'.format(id=id_)
        text = text.replace(search_str, replace_str)
    
    return text

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('请提供两个 JSON 文件的路径作为命令行参数')
        sys.exit(1)
    
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    
    with open(file2_path, 'r') as file:
        mappings = json.load(file)
    
    processed_data = process_json_file(file1_path, mappings)
    
    output_file_name = os.path.splitext(os.path.basename(file1_path))[0] + '_processed.json'
    with open(output_file_name, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=4, ensure_ascii=False)
    
    print('处理完成，结果已保存到', output_file_name)
