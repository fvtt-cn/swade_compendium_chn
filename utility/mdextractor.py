import sys

def extract_content(md_file, output_file):
    with open(md_file, 'r') as file:
        content = file.read()
    
    extracted_content = ''
    lines = content.split('\n')
    for line in lines:
        if line.startswith('###'):
            extracted_content += line[3:] + '\n'
    
    with open(output_file, 'w') as file:
        file.write(extracted_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("请输入正确的命令行参数。示例：python extract_md.py input.md output.md")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        extract_content(input_file, output_file)
        print(f"提取完成，提取内容保存在 {output_file} 文件中。")
