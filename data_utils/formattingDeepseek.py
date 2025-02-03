import os
import re

# Define the categories to extract
CATEGORIES = [
    "Other",
    "Policy Change",
    "First Party Collection/Use",
    "Data Retention",
    "International and Specific Audiences",
    "Third Party Sharing/Collection",
    "User Choice/Control",
    "User Access, Edit and Deletion",
    "Data Security",
    "Do Not Track"
]

# Define possible representations of "Yes" and "No"
YES_VARIANTS = {"true", "yes", "affirmative", "1", "Yes", "True", "YES", "TRUE"}
NO_VARIANTS = {"false", "no", "negative", "0", "No", "False", "NO", "FALSE"}

def clean_and_extract(filepath, output_folder):
    """
    Reads a wrongly formatted file, extracts relevant information, and writes a cleaned version
    to the output folder, ensuring only the last occurrence of each category is considered.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove all text between <think> and </think>
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    # Locate "Final Answer" if present, extract only the section after it
    final_answer_match = re.search(r"Final Answer:?\s*", content, re.IGNORECASE)
    if final_answer_match:
        content = content[final_answer_match.end():].strip()

    # Dictionary to store the last seen value for each category
    last_seen_values = {}

    # Process lines in reverse order to pick the last occurrence first
    for line in reversed(content.split("\n")):
        line = line.strip()
        if ":" in line:  # Ensure it follows "Category: Value" format
            category, value = map(str.strip, line.split(":", 1))
            category = re.sub(r"[*\-(\\)]", "", category).strip()  # Clean category name

            if category in CATEGORIES and category not in last_seen_values:
                # Normalize the value to "Yes" or "No"
                value_lower = value.lower().split()[0] if value else ""
                if value_lower in YES_VARIANTS:
                    last_seen_values[category] = "Yes"
                elif value_lower in NO_VARIANTS:
                    last_seen_values[category] = "No"

    # Ensure all categories are present, default to "No" if missing
    formatted_output = "\n".join(f"{cat}: {last_seen_values.get(cat, 'No')}" for cat in CATEGORIES)

    # Define output file path
    output_filename = os.path.basename(filepath)
    output_path = os.path.join(output_folder, output_filename)

    # Save to the output file
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(formatted_output + "\n")

    print(f"Processed: {filepath} -> {output_path}")

# Example usage
input_folder = "../Output/deepseek/textResults/2shot"  # Change this to the correct input path
output_folder = "../Output/deepseek/newTextResults/2shot"  # Change this to the desired output path

for filename in os.listdir(input_folder):
    if filename.endswith("_result.txt"):
        clean_and_extract(os.path.join(input_folder, filename), output_folder)