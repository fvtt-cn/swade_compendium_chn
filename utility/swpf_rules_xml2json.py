import json
import sys
from bs4 import BeautifulSoup

def title_case(id_str, ignore_list):
    id_words = id_str.split()

    # 首字母大写处理
    for i in range(len(id_words)):
        if id_words[i] not in ignore_list:
            id_words[i] = id_words[i].capitalize()

    return ' '.join(id_words)

def extract_data(html_file, json_file):
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    entryelem = soup.find('h1')
    entry = title_case(entryelem['id'].strip().replace('-', ' '), ['in','of','the', 'and'])
    entries = data.get("entries", {})
    for element in soup.find_all('h3'):
        id_str = element['id']
        id = title_case(id_str.strip().replace('-', ' '), ['in','of','the', 'and'])

        # 查找相应的对象并处理<div>块
        target_obj = entries[entry]['pages'].get(id)
        entries[entry]['name'] = entryelem.text.strip()
        if target_obj is not None:
            div_element = element.find_next_sibling('div', class_='swpf-core')
            if div_element is not None:
                div_element.insert(0, element)
                target_obj['text'] = str(div_element)
                target_obj['name'] = element.text.strip()
    # 更新JSON文件中的entries字段
    data['entries'] = entries

    # 将处理结果保存回JSON文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # 从命令行参数获取文件名
    html_file = sys.argv[1]
    json_file = sys.argv[2]

    # 调用函数进行处理
    extract_data(html_file, json_file)
