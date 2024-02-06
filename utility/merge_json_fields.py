import json
import argparse

def merge_objects(json1, json2, field):
    # 加载第一个json文件
    with open(json1, 'r', encoding='utf-8') as file:
        data1 = json.load(file)

    # 加载第二个json文件
    with open(json2, 'r', encoding='utf-8') as file:
        data2 = json.load(file)

    # 合并actions字段
    for entity in data2['entries']:
        if entity in data1['entries']:
            if field in data2['entries'][entity]:
                if data2['entries'][entity][field] not in ['','\{\}','[]']:
                    data1['entries'][entity][field] = data2['entries'][entity][field]

    # 保存文件
    with open(json1, 'w', encoding='utf-8') as output:
        json1 = json.dump(data1, output, ensure_ascii=False, indent=4)

    print('合并完成。')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='将第二个json文件中的特定字段合并到第一个json文件中的相应实体中')
    parser.add_argument('json1', help='第一个json文件的路径')
    parser.add_argument('json2', help='第二个json文件的路径')
    parser.add_argument('field', help='要合并的字段')
    args = parser.parse_args()

    merge_objects(args.json1, args.json2, args.field)
