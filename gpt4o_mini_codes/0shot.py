import os
import openai
from bs4 import BeautifulSoup

# Define your prompt template
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

def analyze_policy_with_openai(policy_text, api_key):
    """
    Analyze the privacy policy using OpenAI's GPT-4o-mini model via API.
    """
    prompt = PROMPT_TEMPLATE.format(policy_text=policy_text)

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
    output_dir = "../Output/gpt4o_mini/textResults/0shot"

    # Load the API key
    api_key_path = "../api_key.txt"
    with open(api_key_path, "r") as file:
        api_key = file.read().strip()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all policy files in the directory
    policy_files = [f for f in os.listdir(policy_dir) if f.endswith(".html")]

    # Select the first policy as the main policy for the prompt
    main_policy_file = "20_theatlantic.com.html"
    main_policy_path = os.path.join(policy_dir, main_policy_file)

    if main_policy_file not in policy_files:
        raise FileNotFoundError(f"{main_policy_file} not found in {policy_dir}")

    # Parse the main policy HTML
    print(f"Using {main_policy_file} as the main policy...")
    main_policy_text = parse_html_to_text(main_policy_path)

    # Process all other policies for evaluation
    for policy_file in policy_files:
        if policy_file == main_policy_file:
            continue  # Skip the main policy file

        policy_path = os.path.join(policy_dir, policy_file)
        print(f"Analyzing the policy in {policy_path}...")

        try:
            # Parse the current policy HTML
            policy_text = parse_html_to_text(policy_path)

            # Call the model to analyze using the main policy as the context
            output = analyze_policy_with_openai(policy_text, api_key)

            if output:
                # Save output to a text file
                output_filename = policy_file.replace(".html", "_result.txt")
                save_output_to_txt(output, output_dir, output_filename)
            else:
                print(f"No output generated for {policy_file}")

        except Exception as e:
            print(f"Error processing {policy_file}: {e}")