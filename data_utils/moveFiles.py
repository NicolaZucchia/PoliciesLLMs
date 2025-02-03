import os
import shutil

def move_response_files(input_folder, output_folder):
    """
    Moves all files ending in '_response.txt' to another folder while leaving '_formatted.txt' files in place.

    Args:
        input_folder (str): The directory containing the files.
        output_folder (str): The directory where '_response.txt' files will be moved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith("_result.txt"):  # Move only '_response.txt' files
            source_path = os.path.join(input_folder, filename)
            destination_path = os.path.join(output_folder, filename)
            
            shutil.move(source_path, destination_path)  # Move the file
            print(f"Moved: {filename} -> {output_folder}")

# Example usage
input_folder = "../Output/deepseek/newTextResults/1shot"  # Change this to your actual input folder
output_folder = "../Output/deepseek/finalTextResults/1shot"  # Change this to your desired destination folder

move_response_files(input_folder, output_folder)