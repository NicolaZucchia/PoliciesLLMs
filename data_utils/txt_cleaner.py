import os

def clean_txt_files(directory):
    """
    Iterates through text files in the given directory and removes the first line containing 'Data: Answer'.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Process only .txt files
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                
                # Check if the first line contains "Data: Answer"
                if lines and "Data: Answer" in lines[0]:
                    # Remove the first line
                    cleaned_lines = lines[1:]
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.writelines(cleaned_lines)
                    print(f"Cleaned 'Data: Answer' from {filename}")
                else:
                    print(f"No 'Data: Answer' line to clean in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Replace with the path to your directory containing the text files
    text_files_directory = "Output/textResults/1shot"
    clean_txt_files(text_files_directory)