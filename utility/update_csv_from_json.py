import sys
import json
import csv

def update_csv_from_json(json_file, csv_file):
    # 从JSON文件中读取数据
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # 从CSV文件中读取数据
    with open(csv_file, 'r') as f:
        csv_data = list(csv.reader(f))

    # 获取CSV文件的标题行
    header = csv_data[0]
    
    # 确定source列和target列的索引
    source_index = header.index('source')
    target_index = header.index('target')

    # 遍历CSV文件的数据行
    for row in csv_data[1:]:
        source_value = row[source_index]

        # 如果source值与JSON中的某个key匹配，则更新target列的值
        if source_value in json_data:
            target_value = json_data[source_value]
            row[target_index] = target_value

    # 将更新后的数据写入新的CSV文件
    output_file = 'updated_' + csv_file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    print(f"更新后的CSV文件已保存为{output_file}")

if __name__ == '__main__':
    # 确保用户提供了正确的参数
    if len(sys.argv) != 3:
        print("请提供JSON文件和CSV文件的路径作为参数")
    else:
        json_file = sys.argv[1]
        csv_file = sys.argv[2]
        update_csv_from_json(json_file, csv_file)
