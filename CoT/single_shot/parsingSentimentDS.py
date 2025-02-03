import os
import re

def extract_sentiments(input_folder, output_folder):
    """
    Extracts sentiment analysis from policy response files while ignoring text within <think> tags.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith("_response.txt"):  # Process only relevant files
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace("_response.txt", "_filtered.txt"))

            with open(input_path, "r", encoding="utf-8") as infile:
                content = infile.read()

            # Remove everything between <think> and </think>
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)

            # Extract lines that contain category sentiments
            extracted_lines = []
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("**") and ":" in line:
                    category, sentiment_desc = map(str.strip, line.split(":", 1))
                    category = category.replace("**", "")  # Remove special characters
                    extracted_lines.append(f"**{category}: {sentiment_desc}**")

            # Save processed content
            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(extracted_lines) + "\n")

            print(f"Processed: {filename} -> {output_path}")

# Example usage
input_folder = "deepseekResponses"  # Change this to the actual input folder
output_folder = "deepseekParsedResponses"  # Change this to the desired output folder
extract_sentiments(input_folder, output_folder)
