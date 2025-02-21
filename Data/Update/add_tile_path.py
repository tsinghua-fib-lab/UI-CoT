import json
import pandas as pd

# 假设已经读取了json1和json2
json1_file_path = '/data3/maruolong/Train_Data/Updated_dominant_race_data.json'  # 你的json1路径
json2_file_path = '/data3/maruolong/Train_Data/Socioeconomic_median_income_data_all.json'  # 你的json2路径
xlsx_file_path = '/data3/maruolong/Train_Data/filtered_tract_tile_mapping.xlsx'  # 你的GEOID与tile映射文件路径

# 读取JSON文件
with open(json1_file_path, 'r') as f:
    json1_data = json.load(f)

with open(json2_file_path, 'r') as f:
    json2_data = json.load(f)

# 读取GEOID与tile映射的xlsx文件
geoid_tile_df = pd.read_excel(xlsx_file_path)

# 创建一个sample_id到tile的映射
geoid_tile_mapping = dict(zip(geoid_tile_df['GEOID'].astype(str), geoid_tile_df['tile']))

# 用于统计
matched_count = 0
unmatched_count = 0
delete_count = 0

# 需要删除的ID列表
delete_sample_ids = [
    "2016000100", "2105000300", "2150000100", "2261000300", "6083980100", "6111003612", 
    "10005051204", "12037970304", "12087971002", "12087971800", "12087972000", "12087972300", 
    "12087972500", "12087972600", "12087980100", "12099003511", "12103027202", "15003981200", 
    "23029990000", "37055990100", "39123050100", "45043990100", "51001990100", "53055960100", 
    "53055990100", "60010950200", "60030951900", "69085950100", "69110990000", "72097081512", 
    "72137990000"
]

# 遍历json1的数据，进行匹配操作
for sample in json1_data[:]:
    sample_id = sample['sample_id']
    
    # 如果在delete_sample_ids中，删除该sample并更新删除计数
    if sample_id in delete_sample_ids:
        json1_data.remove(sample)
        delete_count += 1
        continue

    # 尝试从json2中找到匹配的sample_id
    matching_sample = next((item for item in json2_data if item['sample_id'] == sample_id), None)
    
    if matching_sample:
        # 如果找到了匹配项，将json2中第一个image路径加入到json1的image列表中
        first_image_path = matching_sample['image'][0]
        sample['image'].insert(0, first_image_path)
        matched_count += 1
    else:
        # 如果没有找到匹配项，尝试根据GEOID从xlsx文件获取tile路径
        geo_id = sample_id[:11].strip()  # 假设GEOID是前11位sample_id
        if geo_id in geoid_tile_mapping:
            tile = geoid_tile_mapping[geo_id]
            # 构造路径并加入到image的第一条
            tile_image_path = f"/data3/maruolong/Train_Data/rs_image/{tile}.png"
            # 如果原来image是空的，删除该sample
            if not sample['image']:  # 如果image列表为空
                json1_data.remove(sample)  # 删除该sample
                delete_count += 1
            else:
                sample['image'].insert(0, tile_image_path)  # 否则，插入路径
                unmatched_count += 1
        else:
            # 如果没有找到对应的GEOID，删除该sample并更新删除计数
            json1_data.remove(sample)
            delete_count += 1

# 输出匹配成功、匹配失败和删除的样本数量
print(f"成功匹配的样本数量: {matched_count}")
print(f"没有匹配的样本数量: {unmatched_count}")
print(f"已删除的样本数量: {delete_count}")

# 保存修改后的JSON文件
with open('/data3/maruolong/Train_Data/Modified_dominant_race_data.json', 'w') as f:
    json.dump(json1_data, f, indent=4)
