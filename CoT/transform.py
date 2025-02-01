import os
import csv
import re

def extract_labels(response_folder, output_csv):
    """
    Extract labels for each category from response files and save them into a CSV file.

    Args:
        response_folder (str): Path to the folder containing GPT response files.
        output_csv (str): Path to the output CSV file.
    """
    # Initialize an empty list to store rows
    rows = []
    # Define category headers
    categories = [
        "Other", "Policy Change", "First Party Collection/Use", "Data Retention",
        "International and Specific Audiences", "Third Party Sharing/Collection",
        "User Choice/Control", "User Access, Edit and Deletion",
        "Data Security", "Do Not Track"
    ]

    # Add headers to the rows list
    headers = ["File"] + categories
    rows.append(headers)

    # Iterate through each file in the response folder
    for file_name in sorted(os.listdir(response_folder)):
        if file_name.endswith(".txt"):
            file_path = os.path.join(response_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Extract the file number
                file_number = re.match(r"(\d+)", file_name).group(1)
                # Initialize a row with the file number
                row = [file_number]

                # Iterate through categories and extract sentiment
                for category in categories:
                    pattern = rf"{category}:\s*(Positive|Neutral|Negative)"
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        sentiment = match.group(1).lower()
                        # Map sentiment to 0 (Positive/Neutral) or 1 (Negative)
                        label = 0 if sentiment in ["positive", "neutral"] else 1
                    else:
                        label = None  # Handle missing categories
                    row.append(label)

                rows.append(row)

    # Write the rows to the output CSV file
    with open(output_csv, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

    print(f"Labels extracted and saved to {output_csv}")


if __name__ == "__main__":
    # Folders containing response files
    gpt4o_folder = "gpt4oResponses"
    gpt35_folder = "gpt35Responses"

    # Output CSV files
    gpt4o_csv = "gpt4o_labels.csv"
    gpt35_csv = "gpt35_labels.csv"

    # Process both folders
    extract_labels(gpt4o_folder, gpt4o_csv)
    extract_labels(gpt35_folder, gpt35_csv)