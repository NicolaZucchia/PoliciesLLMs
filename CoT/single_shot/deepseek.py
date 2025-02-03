import os
import ollama

# Define the revised prompt template for category-wise analysis
CATEGORY_PROMPT_TEMPLATE = """
Let's think step by step.

In the privacy policy:
"{policy_text}"

Analyze the following category:
"{category}"

Locate where it is discussed in the policy and evaluate the sentiment based on the following steps:
- Step 1: Identify the relevant section of the text for this category.
- Step 2: Analyze whether the text suggests a user-friendly or user-risky practice.
- Step 3: Conclude with a sentiment classification for this category (e.g., Positive, Neutral, Negative) and explain why.

In the answer, provide only the final sentiment analysis in the following format:  
Category Name: Sentiment (e.g., Positive, Neutral, Negative) - [Brief Explanation]
"""

def save_output_to_txt(output, output_folder, output_filename):
    """
    Save the output text to a file in the output directory.
    """
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(output)
    print(f"Saved result to {output_path}")

def analyze_policy_category(policy_text, category):
    """
    Analyze a single category in the privacy policy using GPT-3.5 Turbo model via API.
    """
    prompt = CATEGORY_PROMPT_TEMPLATE.format(
        policy_text=policy_text,
        category=category
    )

    try:
        response = ollama.chat(
            model="deepseek-r1:7b",
            messages=[
                {
                "role": "user",
                "content": prompt
                }
            ],
            #max_tokens=1024,  # Limit output tokens
            #temperature=0.0  # Deterministic response
        )
        return response['message']['content']
    except:
        print(f"Error Raised by DeepSeep or Ollama")
        return None

def analyze_policy_with_categories(policy_text, categories):
    """
    Analyze all categories in the privacy policy.
    """
    output_lines = []
    for category in categories:
        category_output = analyze_policy_category(policy_text, category)
        if category_output:
            output_lines.append(category_output)
    return "\n".join(output_lines)

def sort_and_process_files(policy_folder, categories_folder, output_folder):
    """
    Sorts and matches policy files with category files, sends prompts for matching files, and skips unmatched policies.

    Args:
        api_key_path (str): Path to the file containing the API key.
        policy_folder (str): Folder containing policy text files.
        categories_folder (str): Folder containing category text files.
        output_folder (str): Folder to save GPT responses.
    """
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Read the API key
        #with open(api_key_path, 'r', encoding='utf-8') as key_file:
        #    api_key = key_file.read().strip()

        # Get and sort files in both folders
        policy_files = sorted([f for f in os.listdir(policy_folder) if f.endswith(".txt")])
        category_files = sorted([f for f in os.listdir(categories_folder) if f.endswith(".txt")])

        # Process each sorted policy file
        for policy_file in policy_files:
            # Extract the numeric prefix from the policy file
            policy_number = policy_file.split("_")[0]

            # Find a matching category file
            matching_category = next((cat for cat in category_files if cat.startswith(policy_number)), None)

            if matching_category:
                # Load the policy text
                policy_path = os.path.join(policy_folder, policy_file)
                with open(policy_path, 'r', encoding='utf-8') as policy_fp:
                    policy_text = policy_fp.read().strip()

                # Load the categories
                category_path = os.path.join(categories_folder, matching_category)
                with open(category_path, 'r', encoding='utf-8') as category_fp:
                    categories = [line.split(":")[0].strip() for line in category_fp.readlines() if "Yes" in line]

                # Analyze policy and categories
                output = analyze_policy_with_categories(policy_text, categories)

                if output:
                    # Save output to a text file
                    output_filename = policy_file.replace(".txt", "_response.txt")
                    save_output_to_txt(output, output_folder, output_filename)
                else:
                    print(f"No output generated for {policy_file}")

            else:
                print(f"{policy_number}: Found only text, skipping.")

    except Exception as e:
        print(f"Error: {e}")

# Example Usage
if __name__ == "__main__":
    #api_key_path = "../api_key.txt"  # Path to the file containing your API key
    policy_folder = "txtPolicies"  # Folder containing parsed policy text files
    categories_folder = "../../Output/gpt35_turbo/textResults/2shot"  # Best recall
    output_folder = "deepseekResponses"  # Folder to save DS responses

    sort_and_process_files(policy_folder, categories_folder, output_folder)