import os
from htmlParser import html_to_txt 

def parse_html_folder(input_folder, output_folder):
    """
    Parse all HTML files in a folder and save them as plain text in another folder.

    Args:
        input_folder (str): Path to the folder containing HTML files.
        output_folder (str): Path to the folder to save parsed text files.
    """
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Process each HTML file in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".html"):
                input_path = os.path.join(input_folder, file_name)
                output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")

                # Parse HTML to plain text
                print(f"Processing: {file_name}")
                try:
                    html_to_txt(input_path, output_path)
                    print(f"Saved: {output_path}")
                except Exception as e:
                    print(f"Error parsing {file_name}: {e}")

    except Exception as e:
        print(f"Error processing folder: {e}")

# Example usage
if __name__ == "__main__":
    input_folder = "../OPP-115/sanitized_policies"  # Replace with the folder containing your HTML files
    output_folder = "txtPolicies"  # Replace with the folder to save parsed text files

    parse_html_folder(input_folder, output_folder)