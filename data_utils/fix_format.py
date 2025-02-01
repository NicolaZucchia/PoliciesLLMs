import os

def transform_txt_format(input_path, output_path):
    """
    Transforms the text file content:
    - Deletes rows containing `{` or `}`.
    - Removes double quotes and parenthesis.
    - Converts true/false and their variations to Yes/No correctly.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        transformed_lines = []
        for line in lines:
            # Skip rows containing `{` or `}`
            if "{" in line or "}" in line:
                continue

            # Process lines containing key-value pairs
            if ":" in line:
                key, value = line.strip().split(":", 1)
                key = key.strip().replace('"', '')  # Remove double quotes
                value = value.strip().lower()  # Normalize value

                # Map values to true/false
                if value in ["true", "yes", "true,", "yes,"]:
                    transformed_value = "true"
                elif value in ["false", "no", "false,", "no,"]:
                    transformed_value = "false"
                else:
                    transformed_value = value  # Keep unexpected values unchanged

                transformed_lines.append(f"{key}: {transformed_value}")

        # Save the transformed content
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(transformed_lines))
        print(f"Transformed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def process_directory(input_dir, output_dir):
    """
    Processes all `.txt` files in the input directory and transforms them.
    """
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            print(f"Processing {filename}...")
            transform_txt_format(input_path, output_path)


if __name__ == "__main__":
    # Define the input and output directories
    input_dir = "../Output/gpt35_turbo/textResults/2shot"
    output_dir = "../Output/gpt35_turbo/textResults/2shot"

    process_directory(input_dir, output_dir)