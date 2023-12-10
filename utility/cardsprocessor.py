import sys
import json

# 检查命令行参数是否提供了正确的文件路径
if len(sys.argv) < 2:
    print("请提供要处理的json文件路径")
    sys.exit(1)

input_file = sys.argv[1]

# 打开文件并解析json数据
with open(input_file, 'r') as file:
    data = json.load(file)

# 提取每个实体中的name字段作为key值，faces字段作为value值，并保留faces字段中的img和name字段
processed_cards = {}
for card in data["cards"]:
    card_name = card["name"]
    card_faces = []
    for face in card["faces"]:
        card_faces.append({
            "img": face["img"],
            "name": face["name"]
        })
    processed_cards[card_name] = {
        "name": card_name,
        "faces": card_faces
    }

# 将处理过后的cards字段保存在新的json文件中
output_data = {"cards": processed_cards}
output_file = "processed_cards.json"  # 新的json文件名
with open(output_file, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f"处理完成，请查看文件: {output_file}")
