import json
import sys
from bs4 import BeautifulSoup

def extract_data(html_file, json_file):
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data.get("entries", {})
    for div_elem in soup.find_all('div', class_='swpf-core'):
        # 提取id
        h3_elem = div_elem.find('h3', id=True)
        if h3_elem:
            id = h3_elem['id'].strip().replace('-', ' ').title()

            # 在entries中查找相应的对象
            obj = entries.get(id)
            if obj is not None:
                print(id)
                # 将整个<div>块放入"description"字段中
                obj['description'] = str(div_elem)

                # 在<div>块中查找相应的内容并填充字段
                for p_elem in div_elem.find_all('p'):
                    strong_elem = p_elem.find('strong')
                    if strong_elem:
                        content = strong_elem.next_sibling.strip()

                        if strong_elem.text == '位阶：':
                            obj['rank'] = content
                        elif strong_elem.text == '射程：':
                            obj['range'] = content
                        elif strong_elem.text == '特效：':
                            obj['trapping'] = content
                        elif strong_elem.text == '持续时间：':
                            obj['duration'] = content

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
