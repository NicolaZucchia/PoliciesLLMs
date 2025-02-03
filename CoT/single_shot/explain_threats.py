import os
import re

def extract_explanations(input_folder, model_name, category):
    """
    Extracts and prints the explanations for a specific category where a threat was identified.

    Args:
        input_folder (str): Path to the folder containing model outputs.
        model_name (str): Name of the model (used for display).
        category (str): The category to filter explanations for.
    """
    category_pattern = re.compile(rf"\*\*{category}: (Positive|Neutral|Negative) -\*\* (.+)", re.IGNORECASE)

    explanations = []

    for filename in os.listdir(input_folder):
        if filename.endswith("_response.txt"):  # Ensure only response files are processed
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.readlines()
            
            for line in content:
                match = category_pattern.match(line.strip())
                if match:
                    sentiment = match.group(1)
                    explanation = match.group(2)
                    explanations.append(f"File: {filename} | Sentiment: {sentiment} | Explanation: {explanation}")

    # Print results
    if explanations:
        print(f"\n--- {model_name} Threat Explanations for '{category}' ---\n")
        for explanation in explanations:
            print(explanation)
        print("\n--------------------------------------------\n")
    else:
        print(f"No threats detected for '{category}' in {model_name} outputs.")

# Example Usage
deepseek_folder = "deepseekResponses"  # Folder containing DeepSeek model outputs
# gpt4o_folder = "gpt4oResponses"  # Folder containing GPT-4o outputs
category_to_check = "Policy Change"  # Change this to any category

extract_explanations(deepseek_folder, "DeepSeek R1-7B", category_to_check)
# extract_explanations(gpt4o_folder, "GPT-4o", category_to_check)