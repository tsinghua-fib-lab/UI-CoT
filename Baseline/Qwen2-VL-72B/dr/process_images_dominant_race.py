import json
import random

def calculate_dominant_race(tract, race_counts):
    """根据种族统计结果计算主导种族"""
    total_samples = sum(race_counts.values())
    threshold = total_samples / 5  # 超过五分之一的阈值

    # 筛选符合条件的非白人种族
    minority_races = {race: count for race, count in race_counts.items()
                      if race in {"Black or African American", "Asian", "Hispanic or Latino"} and count >= threshold}

    if not minority_races:  # 如果没有任何非白人种族超过五分之一
        return "White alone, not Hispanic or Latino"

    if len(minority_races) == 1:  # 如果只有一个少数族裔满足条件
        return max(minority_races, key=minority_races.get)

    # 如果多个少数族裔满足条件，选择数量最多的那个
    sorted_candidates = sorted(minority_races.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_candidates) > 1 and sorted_candidates[0][1] == sorted_candidates[1][1]:
        # 如果数量相等，随机选择一个
        return random.choice(list(minority_races.keys()))
    return sorted_candidates[0][0]

def process_jsonl(input_path, output_path):
    """处理 JSONL 文件，统计主导种族并输出结果"""
    valid_races = {
        "White alone, not Hispanic or Latino",
        "Black or African American",
        "Asian",
        "Hispanic or Latino"
    }

    results = []
    current_tract = None
    race_counts = {}

    with open(input_path, 'r') as infile:
        for line in infile:
            sample = json.loads(line.strip())
            tract = sample["tract"]
            race = sample["race"]
            # 忽略无效的种族
            if race not in valid_races:
                continue

            if current_tract is None:  # 第一次读取 tract
                current_tract = tract

            if tract != current_tract:  # 如果进入了新的 tract
                # 计算当前 tract 的主导种族
                dominant_race = calculate_dominant_race(current_tract, race_counts)
                results.append({"tract": current_tract, "dominant_race": dominant_race})

                # 重置为新 tract
                current_tract = tract
                race_counts = {}

            # 累加种族样本计数
            race_counts[race] = race_counts.get(race, 0) + 1

        # 处理最后一个 tract
        if current_tract is not None:
            dominant_race = calculate_dominant_race(current_tract, race_counts)
            results.append({"tract": current_tract, "dominant_race": dominant_race})

    # 输出结果到 JSONL 文件
    with open(output_path, 'w') as outfile:
        for result in results:
            outfile.write(json.dumps(result) + '\n')

# 示例调用
input_file = "/data3/maruolong/Train_Data/Add_Path/Qwen2-VL-7B/matched_images_with_levels.jsonl"
output_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/tract_dominant_race_images_match_method1.jsonl"
process_jsonl(input_file, output_file)
