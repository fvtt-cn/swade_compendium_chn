import sys
import yaml
import json

def yaml_to_json(yaml_file, json_file):
    # 读取YAML文件
    with open(yaml_file, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    
    # 将YAML转换为JSON
    json_data = json.dumps(yaml_data, indent=4, ensure_ascii=False)
    
    # 保存为JSON文件
    with open(json_file, 'w', encoding='utf-8') as file:
        file.write(json_data)

# 命令行参数检查
if len(sys.argv) < 2:
    print("请提供YAML文件作为命令行参数！")
    sys.exit(1)

# 获取命令行参数
yaml_file = sys.argv[1]
filename = yaml_file.split(".")[0]
json_file = filename + ".json"

# 转换YAML为JSON并保存
yaml_to_json(yaml_file, json_file)

# 完成提示
print("转换完成！JSON文件已保存为:", json_file)
