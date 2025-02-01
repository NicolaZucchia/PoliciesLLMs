import os

def format_and_clean_txt_files(input_dir, output_dir):
    """
    Cleans and formats text files to match the desired output format.
    Removes blank rows and converts 'true/false' to 'Yes/No'.

    Args:
        input_dir: Directory containing the input text files.
        output_dir: Directory to save the cleaned files.
    """
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                with open(input_path, "r", encoding="utf-8") as infile:
                    lines = infile.readlines()

                cleaned_lines = []
                for line in lines:
                    # Remove blank lines and format the content
                    line = line.strip()
                    if line:  # Skip empty lines
                        if ": true" in line.lower():
                            cleaned_lines.append(line.replace(": true", ": Yes").replace(": True", ": Yes"))
                        elif ": false" in line.lower():
                            cleaned_lines.append(line.replace(": false", ": No").replace(": False", ": No"))
                        else:
                            cleaned_lines.append(line)

                # Write the cleaned and formatted content to the output file
                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write("\n".join(cleaned_lines))

                print(f"Formatted and saved: {output_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    # Set the input and output directories
    input_dir = "../Output/gpt35_turbo/textResults/2shot"
    output_dir = "../Output/gpt35_turbo/textResults/2shot"

    format_and_clean_txt_files(input_dir, output_dir)