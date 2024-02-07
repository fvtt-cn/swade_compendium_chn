import json
import argparse
from bs4 import BeautifulSoup

def add_image_tag(json1_path, json2_path):
    # 读取第一个JSON文件
    with open(json1_path, 'r') as file1:
        json1 = json.load(file1)

    # 读取第二个JSON文件
    with open(json2_path, 'r') as file2:
        json2 = json.load(file2)

    # 检查两个JSON文件的entries对象是否存在，并且长度相同
    if 'entries' not in json1 or 'entries' not in json2:
        print("JSON文件格式错误，必须包含entries对象")
        return

    # 循环遍历每个entry，并检查第二个JSON文件的对应entry是否包含<img>标签，若有则添加到第一个JSON文件的相应entry的text字段中
    for entry_key in json1['entries']:
        if entry_key in json2['entries']:
            for page in json2['entries'][entry_key]['pages']:
                img_tag = json2['entries'][entry_key]['pages'][page]['text']
                if '<img' in img_tag:
                    # 解析第一个JSON文件的text字段
                    soup1 = BeautifulSoup(json1['entries'][entry_key]['pages'][page]['text'], 'html.parser')
                    # 解析第二个JSON文件的img标签
                    soup2 = BeautifulSoup(img_tag, 'html.parser')
                    # 将第二个JSON文件的img标签插入到第一个JSON文件的text中
                    imgs = soup2.find_all("img")
                    #print(str(imgs))
                    #print(str(soup1))
                    div = soup1.find('div',class_='swpf-core')
                    if div is not None:
                        #print(str(div))
                        for img in imgs:
                            div.insert(1,img)
                    # 更新第一个JSON文件的text字段
                    json1['entries'][entry_key]['pages'][page]['text'] = str(soup1)

    # 将结果写回第一个JSON文件
    with open(json1_path, 'w') as file1:
        json.dump(json1, file1, ensure_ascii=False)

    print("处理完成")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='添加第二个JSON文件中的<img>标签到第一个JSON文件的entries中')
    parser.add_argument('json1', type=str, help='第一个JSON文件的路径')
    parser.add_argument('json2', type=str, help='第二个JSON文件的路径')
    args = parser.parse_args()

    add_image_tag(args.json1, args.json2)
