import csv
import sys

def remove_quotes(string):
    # 去除字符串中的双引号
    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    return string

def fill_empty_values(file1, file2):
    # 读取第一个文件，构建字典
    data = {}
    with open(file1, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['source']
            value = remove_quotes(row['target'])
            data[key] = value
    
    # 读取第二个文件，填充空值
    updated_rows = 0
    with open(file2, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)  # 转换为列表，以支持随机访问

    for row in rows:
        source = row['source']
        target = remove_quotes(row['target'])
        if source in data and target == '':
            row['target'] = data[source]
            updated_rows += 1
    
    # 更新第二个文件
    with open(file2, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"成功填充了 {updated_rows} 行空值。")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("请提供正确的文件名作为命令行参数。")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    fill_empty_values(file1, file2)
