import sys
import csv
import yaml

def csv_to_yaml(csv_file, yaml_file):
    data = {}
    with open(csv_file, 'r') as file:
        # 读取CSV文件
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # 使用context列作为YAML的key，source列作为YAML的value
            key = row['context']
            value = row['source']
            data[key] = value

    with open(yaml_file, 'w') as file:
        # 写入YAML文件
        yaml.dump(data, file)

if __name__ == '__main__':
    # 通过命令行参数获取CSV文件和YAML文件的路径
    if len(sys.argv) != 3:
        print("请提供CSV文件和YAML文件的路径作为命令行参数")
        sys.exit(1)

    csv_file = sys.argv[1]
    yaml_file = sys.argv[2]
    csv_to_yaml(csv_file, yaml_file)
