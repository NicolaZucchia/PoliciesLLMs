import os

def clean_backticks(input_folder, output_folder):
    """
    Removes lines that contain only backticks (`) and cleans lines that contain backticks but also have other text.

    Args:
        input_folder (str): Path to the folder containing text files.
        output_folder (str): Path to save the cleaned files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Process only .txt files
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r", encoding="utf-8") as infile:
                lines = infile.readlines()

            cleaned_lines = []
            for line in lines:
                stripped_line = line.strip()
                if stripped_line != "```":  # Skip lines with only ```
                    cleaned_lines.append(line.replace("```", "").strip())  # Remove backticks, keep text

            # Save cleaned content
            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(cleaned_lines) + "\n")

            print(f"Processed: {filename} -> {output_path}")

# Example usage
input_folder = "../Output/deepseek/finalTextResults/2shot"  # Change to your input folder path
output_folder = "../Output/deepseek/dsTextResults/2shot"  # Change to your desired output folder path

clean_backticks(input_folder, output_folder)