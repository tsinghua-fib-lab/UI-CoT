import json
import re

def extract_data(input_file, output_file):
    total_samples = 0
    valid_samples = 0
    result = []

    with open(input_file, 'r') as infile:
        for line in infile:
            total_samples += 1
            if not line.strip():
                continue
            try:
                data = json.loads(line.strip())
                question_id = data.get("tract")
                text = data.get("predict", "")
                ground_truth = data.get("label", "")

                # Extracting "predict" from "text"
                predict = {}
                # 提取预测的收入分布和基尼系数数据
                try:
                    # 查找收入分布部分的起始点
                    income_start = text.find("Income distribution:\n")
                    if income_start == -1:
                        print("No income distribution found")
                        continue

                    # 提取 Income distribution 数据部分
                    income_data_section = text[income_start:]

                    # 使用正则表达式匹配 LEVEL1 到 LEVEL10 和 Gini coefficient
                    income_pattern = r"LEVEL(\d+):\s*([\d.]+)"
                    gini_pattern = r"Gini coefficient:\s*([\d.]+)"

                    # 提取 LEVEL1 到 LEVEL10 的数据
                    income_matches = re.findall(income_pattern, income_data_section)
                    if not income_matches:
                        print("No income levels found")
                        continue

                    # 初始化数据字典
                    predict = {}
                    for level, value in income_matches:
                        predict[f"LEVEL{level}"] = float(value)

                    # 提取 Gini 系数数据
                    gini_match = re.search(gini_pattern, income_data_section)
                    if gini_match:
                        predict["GINI"] = float(gini_match.group(1))
                    else:
                        print("No Gini coefficient found")
                        continue

                except Exception as e:
                    print(f"Error processing sample: {e}")
                    continue

                # Extracting "label" from "ground_truth"
                label = {}
                try:
                    income_data_section = ground_truth[:]
                    income_pattern = r"LEVEL(\d+):\s*([\d.]+)"
                    gini_pattern = r"Gini coefficient:\s*([\d.]+)"

                    # 提取 LEVEL1 到 LEVEL10 的数据
                    income_matches = re.findall(income_pattern, income_data_section)
                    if not income_matches:
                        print("No income levels found")
                        continue

                    for level, value in income_matches:
                        label[f"LEVEL{level}"] = float(value)

                    # 提取 Gini 系数数据
                    gini_match = re.search(gini_pattern, income_data_section)
                    if gini_match:
                        label["GINI"] = float(gini_match.group(1))
                    else:
                        print("No Gini coefficient found")
                        continue

                except (ValueError, IndexError):
                    continue  # Skip this sample if ground_truth extraction fails

                # Append result
                result.append({
                    "tract": question_id,
                    "predict": predict,
                    "label": label
                })
                valid_samples += 1
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")
            except KeyError as e:
                print(f"Missing expected key in sample {data.get('tract', 'Unknown')}: {e}")
            except Exception as e:
                print(f"Error processing sample {data.get('tract', 'Unknown')}: {e}")

    # Write to new JSONL file
    with open(output_file, 'w') as outfile:
        for item in result:
            outfile.write(json.dumps(item) + '\n')

    print(f"Total samples in input file: {total_samples}")
    print(f"Samples written to output file: {valid_samples}")


# Example usage
input_file = "/data3/maruolong/Train_Data/change_path_number/bw/result/5_images_gc_CoT_result.jsonl"  # Replace with your input file path
output_file = "/data3/maruolong/Train_Data/change_path_number/gc/result/5_images_gc_CoT_result_update.jsonl"  # Replace with your desired output file path
extract_data(input_file, output_file)
