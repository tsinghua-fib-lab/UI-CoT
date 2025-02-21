import json

# File paths
sample_file = "/data3/maruolong/Train_Data/Add_Path/NEW_Test/dr_2000_test.json"  # Original sample JSON file path
output_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_test/dr_2000_test_change_prompt.json"  # New sample JSON file path

# Load sample file
with open(sample_file, "r") as f:
    samples = json.load(f)

# Update each sample's first value content
for sample in samples:
    # Get the value content of the first conversation
    value = sample["conversations"][0]["value"]
    
    # Find the last '\n' and replace the content after it
    if "\n" in value:
        updated_value = value.rsplit("\n", 1)[0] + "\n" + (
            "Follow the steps below to estimate the dominant race for this area.\n "
            "STEP1: First estimate the population proportions of the four races in this tract based on the images provided.\n "
            "STEP2: Identify the race with the highest estimated proportion and match it with the corresponding choice from the list.\n "
            "Please provide your predicted correct choice and the estimated population proportions of the four races in this tract. "
            "Strictly output only the choice and the estimated proportions, do not include analysis content. Example output format:\n"
            "- Choice: X\n"
            "- Population Proportions:\n"
            "  - White alone, not Hispanic or Latino: XX.X%\n"
            "  - Black or African American: XX.X%\n"
            "  - Asian: XX.X%\n"
            "  - Hispanic or Latino: XX.X%"
        )
        sample["conversations"][0]["value"] = updated_value

# Save the updated samples to a new JSON file
with open(output_file, "w") as f:
    json.dump(samples, f, indent=4)

print(f"Updated samples saved to {output_file}")
