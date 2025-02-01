import os
import openai
from bs4 import BeautifulSoup
import json

# Define your 1-shot prompt template
PROMPT_TEMPLATE = """
The following text between double quotation marks is a privacy policy:
"{policy_text}"

Does the privacy policy affirm that any of these personal data are collected?
— Other
— Policy Change
— First Party Collection/Use
— Data Retention
— International and Specific Audiences
— Third Party Sharing/Collection
— User Choice/Control
— User Access, Edit and Deletion
— Data Security
— Do Not Track

Please adapt your answer to the following format:
Data: Answer

Where Data is any of the data types above and Answer must be only either "Yes" or "No".

Here is an example of processing a privacy policy:

Example Policy:
"{example_policy}"

Expected Output:
Data: Answer
{example_gt}
"""

def parse_html_to_text(html_file_path):
    """
    Parse the privacy policy content from an HTML file.
    """
    with open(html_file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()

def load_example_gt(json_file_path):
    """
    Load the ground truth (Data: Answer) from a JSON file.
    """
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        formatted_gt = "\n".join([f"{key}: {str(value).lower()}" for key, value in data.items()])
        return formatted_gt

def save_output_to_txt(output, output_dir, output_filename):
    """
    Save the output text to a file in the output directory.
    Exclude initial lines starting with "Data: Answer" and save only the relevant results.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    lines = output.splitlines()
    # Skip the initial "Data: Answer" line
    relevant_lines = [line for line in lines if not line.startswith("Data: Answer")]
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(relevant_lines))
    print(f"Saved result to {output_path}")

def analyze_policy_with_openai(policy_text, example_policy, example_gt, api_key):
    """
    Analyze the privacy policy using OpenAI's GPT-4o-mini model via API with a 1-shot prompt.
    """
    prompt = PROMPT_TEMPLATE.format(
        policy_text=policy_text,
        example_policy=example_policy,
        example_gt=example_gt
    )
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for privacy policy analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,  # Limit output tokens
            temperature=0.0  # Deterministic response
        )
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None

if __name__ == "__main__":
    # Directory containing the policy HTML files
    policy_dir = "../OPP-115/sanitized_policies"
    output_dir = "../Output/gpt4o_mini/textResults/1shot"

    # Paths for the example policy and its ground truth
    example_policy_path = "../OPP-115/sanitized_policies/98_neworleansonline.com.html"
    example_gt_path = "../Categories/98_neworleansonline.com.json"

    # Load the API key
    api_key_path = "../api_key.txt"
    with open(api_key_path, "r") as file:
        api_key = file.read().strip()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Parse the example policy and ground truth
    example_policy_text = parse_html_to_text(example_policy_path)
    example_gt_text = load_example_gt(example_gt_path)

    # Process all files in the directory
    policy_files = [f for f in os.listdir(policy_dir) if f.endswith(".html")]
    for policy_file in policy_files:
        # Skip the example policy file to avoid redundant processing
        if policy_file == os.path.basename(example_policy_path):
            continue

        policy_path = os.path.join(policy_dir, policy_file)
        print(f"Analyzing the policy in {policy_path}...")

        try:
            # Parse the policy HTML
            policy_text = parse_html_to_text(policy_path)

            # Call the model to analyze
            output = analyze_policy_with_openai(policy_text, example_policy_text, example_gt_text, api_key)

            if output:
                # Save output to a text file
                output_filename = policy_file.replace(".html", "_result.txt")
                save_output_to_txt(output, output_dir, output_filename)
            else:
                print(f"No output generated for {policy_file}")

        except Exception as e:
            print(f"Error processing {policy_file}: {e}")