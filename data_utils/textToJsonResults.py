import os
import json

def convert_txt_to_json(input_dir, output_dir):
    """
    Convert text files in the input directory to JSON files in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    for txt_file in os.listdir(input_dir):
        if txt_file.endswith(".txt"):
            txt_path = os.path.join(input_dir, txt_file)
            with open(txt_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Convert text format to JSON format
            json_data = {}
            for line in lines:
                if ": " in line:
                    key, value = line.strip().split(": ", 1)
                    json_data[key.strip()] = value.strip() == "Yes"

            # Save JSON file
            json_filename = txt_file.replace("_result.txt", "_result.json")
            json_path = os.path.join(output_dir, json_filename)
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4)
            print(f"Converted {txt_file} to {json_filename}")

if __name__ == "__main__":
    input_dir = "../Output/gpt35_turbo/textResults/2shot"
    output_dir = "../Output/gpt35_turbo/jsonResults/2shot"
    convert_txt_to_json(input_dir, output_dir)