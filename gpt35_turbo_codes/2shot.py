import os
import openai
from bs4 import BeautifulSoup

# Define your 2-shot prompt template
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

Here are two examples:

Example 1.
Policy paragraph:
"{example_policy1}"

Expected Output:
Data: Answer
{example_gt1}

Example 2.
Policy paragraph:
"{example_policy2}"

Expected Output:
Data: Answer
{example_gt2}
"""

def parse_html_to_text(html_file_path):
    """
    Parse the privacy policy content from an HTML file.
    """
    with open(html_file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()

def save_output_to_txt(output, output_dir, output_filename):
    """
    Save the output text to a file in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(output)
    print(f"Saved result to {output_path}")

def analyze_policy_with_openai(policy_text, example_policy1, example_gt1, example_policy2, example_gt2, api_key):
    """
    Analyze the privacy policy using OpenAI's GPT-3.5 Turbo model via API.
    """
    prompt = PROMPT_TEMPLATE.format(
        policy_text=policy_text,
        example_policy1=example_policy1,
        example_gt1=example_gt1,
        example_policy2=example_policy2,
        example_gt2=example_gt2
    )

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
    output_dir = "../Output/gpt35_turbo/textResults/2shot"

    # Load the API key
    api_key_path = "../api_key.txt"
    with open(api_key_path, "r") as file:
        api_key = file.read().strip()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all policy files in the directory
    policy_files = [f for f in os.listdir(policy_dir) if f.endswith(".html")]

    # Select the first two policies as examples
    example_policy_file1 = "20_theatlantic.com.html"
    example_policy_file2 = "760_si.edu.html"

    example_policy_path1 = os.path.join(policy_dir, example_policy_file1)
    example_policy_path2 = os.path.join(policy_dir, example_policy_file2)

    if example_policy_file1 not in policy_files or example_policy_file2 not in policy_files:
        raise FileNotFoundError("Example policies not found in the directory")

    # Parse the example policy HTMLs
    example_policy_text1 = parse_html_to_text(example_policy_path1)
    example_policy_text2 = parse_html_to_text(example_policy_path2)

    # Load ground truths for the examples
    example_gt_path1 = "../Categories/20_theatlantic.com.json"
    example_gt_path2 = "../Categories/760_si.edu.json"

    with open(example_gt_path1, "r", encoding="utf-8") as file:
        example_gt1 = file.read()

    with open(example_gt_path2, "r", encoding="utf-8") as file:
        example_gt2 = file.read()

    # Process all other policies for evaluation
    for policy_file in policy_files:
        if policy_file in [example_policy_file1, example_policy_file2]:
            continue  # Skip the example policies

        policy_path = os.path.join(policy_dir, policy_file)
        print(f"Analyzing the policy in {policy_path}...")

        try:
            # Parse the current policy HTML
            policy_text = parse_html_to_text(policy_path)

            # Call the model to analyze using the two example policies
            output = analyze_policy_with_openai(
                policy_text, example_policy_text1, example_gt1, example_policy_text2, example_gt2, api_key
            )

            if output:
                # Save output to a text file
                output_filename = policy_file.replace(".html", "_result.txt")
                save_output_to_txt(output, output_dir, output_filename)
            else:
                print(f"No output generated for {policy_file}")

        except Exception as e:
            print(f"Error processing {policy_file}: {e}")