import json
import re

# 文件路径
normalized_data_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/normalized_race_ratio.jsonl"  # 归一化的JSONL文件路径
sample_file = "/data3/maruolong/Train_Data/Add_Path/NEW_Train/dr_5008_train.json"  # 样本JSON文件路径
output_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_train/dr_CoT_train.json"  # 生成的新样本JSON文件路径

# 加载归一化数据
normalized_data = {}
with open(normalized_data_file, "r") as f:
    for line in f:
        record = json.loads(line)
        normalized_data[record["tract"]] = record

# 加载样本文件
with open(sample_file, "r") as f:
    samples = json.load(f)

# 存储种族不匹配的tract_id
mismatched_tracts = []

# 处理样本，替换CoT内容
for sample in samples:
    tract_id = sample["sample_id"]
    gpt_choice = sample["conversations"][-1]["value"]  # 获取模型选择的选项（即A、B、C、D）

    if tract_id in normalized_data:
        # 获取归一化数据
        data = normalized_data[tract_id]
        white = data["White alone, not Hispanic or Latino"]
        black = data["Black or African American"]
        asian = data["Asian"]
        hispanic = data["Hispanic or Latino"]

        # 提取选项并映射到对应的种族
        option_values = sample["conversations"][0]["value"]  # 获取包含种族选项的句子

        # 使用正则表达式提取每个选项（格式：字母+点+空格+种族名）
        options = re.findall(r"([A-D])\.\s*([^\n]+)", option_values)

        # 创建种族映射
        race_map = {}
        for letter, race in options:
            race_map[letter] = race.strip()

        # 根据选项映射确定主导种族
        dominant_race_from_gpt = race_map.get(gpt_choice, "Unknown")

        # 计算占比最大的种族
        max_race = max([(white, "White alone, not Hispanic or Latino"),
                        (black, "Black or African American"),
                        (asian, "Asian"),
                        (hispanic, "Hispanic or Latino")], key=lambda x: x[0])[1]

        # 比较两种方法得到的种族名是否一致
        if dominant_race_from_gpt != max_race:
            mismatched_tracts.append(tract_id)

        # 构造CoT内容
        cot_content = (
    f"1. **<Summary>**\n"
    f"Based on the images, if we aim to determine the dominant race in this tract, we focus on key characteristics such as the architectural style and condition of the houses, "
    f"the presence of cultural elements like religious symbols, murals, decorations, bilingual signage, visible language features on signs and advertisements, "
    f"and the overall infrastructure and environment of the neighborhood.\n\n\n"

    f"2. **<Caption>**\n"
    f"These observations lead to the following estimated population proportions for the tract:\n\n"
    f"- White alone, not Hispanic or Latino: {white}%\n"
    f"- Black or African American: {black}%\n"
    f"- Asian: {asian}%\n"
    f"- Hispanic or Latino: {hispanic}%\n\n\n"

    f"3. **<Calculation>**\n"
    f"Based on the predicted population proportions, we identify the group with the highest proportion. "
    f"Therefore, the dominant race in the tract is **{max_race}**, corresponding to option **{gpt_choice}**.\n\n\n"

    f"4. **<Answer>**\n"
    f"Output:\n"
    f"- Choice: {gpt_choice}\n"
    f"- Population Proportions:\n"
    f"  - White alone, not Hispanic or Latino: {white}%\n"
    f"  - Black or African American: {black}%\n"
    f"  - Asian: {asian}%\n"
    f"  - Hispanic or Latino: {hispanic}%\n"
)


        # 替换第二个位置的value为生成的CoT内容
        if len(sample["conversations"]) > 1:
            sample["conversations"][1]["value"] = cot_content
        else:
            # 如果第二个位置不存在，创建新的对话记录
            sample["conversations"].append({"role": "assistant", "value": cot_content})

# 保存更新后的样本到新的JSON文件
with open(output_file, "w") as f:
    json.dump(samples, f, indent=4)

# 输出不匹配的tract_id
if mismatched_tracts:
    print(f"Tracts with mismatched dominant race: {mismatched_tracts}")
else:
    print("No mismatched tracts found.")

print(f"Updated samples saved to {output_file}")