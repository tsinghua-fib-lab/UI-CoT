import json

def generate_calculation_section(data):
    results = []

    for record in data:
        tract_id = record["tract_id"]
        proportions = record["income_distribution"]
        income_values = record["income_values"]

        # Step 1: Calculate Income × Proportion
        income_proportions = [
            income * proportion for income, proportion in zip(income_values, proportions)
        ]

        # Step 2: Cumulative Income and Total Income
        total_income = sum(income_proportions)
        cumulative_income = []
        cumulative_sum = 0
        for income in income_proportions:
            cumulative_sum += income
            cumulative_income.append(cumulative_sum)
        cumulative_proportions = [
            income / total_income for income in cumulative_income
        ]

        # Step 3: Apply Gini Coefficient Formula
        gini_sum_terms = [
            p * (y_curr + y_prev)
            for p, y_curr, y_prev in zip(
                proportions, cumulative_proportions, [0] + cumulative_proportions[:-1]
            )
        ]
        gini_sum = sum(gini_sum_terms)
        gini = 1 - gini_sum
        
        # Create the substitute values for display
        substitute_values = " + ".join(
            [f"{proportions[i]:.4f} × ({cumulative_proportions[i]:.4f} + {cumulative_proportions[i-1] if i > 0 else 0:.4f})" for i in range(len(proportions))]
        )

        # Simplified calculation (sum of terms)
        simplified_calculation = " + ".join([f"{term:.4f}" for term in gini_sum_terms])

        # Formatting the output for <Calculation>
        result = f"""
Let's think step by step.

### 1. **<Summary>**  
#### Objective: Define the general process for calculating the Gini coefficient based on images.
- **Process**: Given the set of images representing a U.S. census tract, I will analyze them to look for visual cues that reflect socioeconomic conditions. Then, I will predict the proportions for each income level based on the insights derived from the images. Finally, I will calculate the Gini coefficient based on this distribution, reflecting the overall income inequality.   

---

### 2. **<Caption>**
#### Objective: Predict the income distribution based on the insights gained from image perception.

1. I perceive visual cues from the satellite and street view images, focusing on factors such as land use patterns, housing quality, street cleanliness, infrastructure, green space distribution, and the presence of amenities like schools, parks, and public transportation.

2. Based on the perceptual insights obtained from the images, and combined with the 10 income ranges you provided, I estimate the income distribution across 10 levels as (the total proportions sum to 1):
   {', '.join([f"LEVEL{i+1}: {proportion:.2f}" for i, proportion in enumerate(proportions)])}

2. Then, I combine the given representative income values with the income distribution proportions obtained in the previous step for each level, resulting in the following structured format:
- {', '.join([f'({income}, {proportion:.2f})' for income, proportion in zip(income_values, proportions)])}

---

### 3. **<Calculation>**
#### Objective: Calculate the Gini coefficient based on the predicted income distribution.
- **Input**: Structured data from **<Caption>**.
- **Tasks**:
  1. **Construct income proportions**:
     - **population proportions (given)** ( p_i ):
       {"; ".join([f"LEVEL{i+1}: {proportion:.4f}" for i, proportion in enumerate(proportions)])}
     
     - **Representative Income × Population Proportion**:
       {"; ".join([f"LEVEL{i+1}: {income_values[i]} × {proportions[i]:.4f} = {income_proportions[i]:.2f}" for i in range(len(proportions))])}
     
     - **Cumulative Income**:
       {"; ".join([f"LEVEL{i+1}: {' + '.join([f'{income_proportions[j]:.0f}' for j in range(i+1)])} = {cumulative_income[i]:.0f}" for i in range(len(cumulative_income))])}
     
     - **Cumulative Income Proportions ( y_i )**:
       {"; ".join([f"LEVEL{i+1}: {cumulative_income[i]:.0f} / {total_income:.0f} = {cumulative_proportions[i]:.4f}" for i in range(len(cumulative_proportions))])}

  2. **Apply the Gini coefficient formula**:
     - Use the formula ( G = 1 - sum_{{i=2}}^{10} p_i × (y_i + y_{{i-1}}) ), where:
       - ( p_i ): Population proportion.
       - ( y_i ): Cumulative income proportion.
     
       Substituting the calculated values:
       - G = 1 - [{substitute_values}]
     
       Simplified Calculation:
       - G = 1 - ({simplified_calculation})
     
       Final Result:
       - G = 1 - {gini_sum:.4f} = {gini:.4f}

- **Gini coefficient**:
   G = {gini:.2f}

---

### 4. **<Answer>**
#### Objective: Present the predicted income distribution and the final Gini coefficient as the result.

- Income distribution:
   {', '.join([f'LEVEL{i+1}: {proportion:.2f}' for i, proportion in enumerate(proportions)])}

- Gini coefficient: {gini:.2f}

"""

        results.append({"tract_id": tract_id, "calculation_section": result.strip()})
    
    return results


# Read the input JSONL file
input_file = '/data3/maruolong/Train_Data/Add_Path/Qwen2-VL-7B/income_distribution.jsonl'  # Replace with your actual file path
output_file = '/data3/maruolong/Train_Data/Add_Path/baseline/train_tract_CoT.jsonl'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        data = json.loads(line.strip())
        
        # Mapping income ranges to levels
        income_distribution = [
            data["Less than $10,000"] / 100, data["$10,000 to $14,999"] / 100, data["$15,000 to $24,999"] / 100,
            data["$25,000 to $34,999"] / 100, data["$35,000 to $49,999"] / 100, data["$50,000 to $74,999"] / 100,
            data["$75,000 to $99,999"] / 100, data["$100,000 to $149,999"] / 100, data["$150,000 to $199,999"] / 100,
            data["$200,000 or more"] / 100
        ]
        
        # Mapping income levels to representative income values
        income_values = [5000, 12500, 20000, 30000, 42500, 62500, 87500, 125000, 175000, 350000]
        
        # Prepare data for calculation
        calculation_data = [{
            "tract_id": data["tract"],
            "income_distribution": income_distribution,
            "income_values": income_values
        }]
        
        # Generate the result using the function
        results = generate_calculation_section(calculation_data)
        
        # Output the results to a new JSONL file
        for result in results:
            output_data = {"tract": result["tract_id"], "result": result["calculation_section"]}
            outfile.write(json.dumps(output_data) + "\n")

print(f"Results have been written to {output_file}")