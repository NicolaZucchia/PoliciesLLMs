import os
import openai

# OpenAI API key (ensure you have set it up correctly)
openai.api_key = "...Enter your API key here..."

def reformat_categories_with_gpt(policy_text, deepseek_output, expected_output):
    """
    Sends the policy output to GPT for category extraction and formatting.
    """
    prompt = f"""
    You will be given an extracted output from a DeepSeek model analyzing a privacy policy.  
    However, the extracted categories are not well formatted and need correction.  

    Your Task is to identify the predefined categories exactly as stated below:
      1. Other
      2. Policy Change
      3. First Party Collection/Use
      4. Data Retention
      5. International and Specific Audiences
      6. Third Party Sharing/Collection
      7. User Choice/Control
      8. User Access, Edit and Deletion
      9. Data Security
      10. Do Not Track

    - Ensure each category is assigned **either "Yes" or "No"**.
    - If multiple mentions exist, take only the last occurrence for each category.
    - You may find alternative words instead of "Yes" and "No": the most common are "True" and "False"
    - It is up to you to understand whether the assign evaluation falls into "Yes" or "No" (True and variants for Yes, False and variants for No)
    - Standardize the output into the following format:

    ```
    Other: Yes
    Policy Change: Yes
    First Party Collection/Use: No
    Data Retention: Yes
    International and Specific Audiences: No
    Third Party Sharing/Collection: Yes
    User Choice/Control: No
    User Access, Edit and Deletion: Yes
    Data Security: Yes
    Do Not Track: No
    ```

    **Example Input in Wrong Format:**
    ```
    {deepseek_output}
    ```

    **Expected Output in Right Format:**
    ```
    {expected_output}
    ```

    Here is the text you have to process:

    {policy_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an assistant that extracts structured insights from privacy policies."},
                  {"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.0
    )

    return response['choices'][0]['message']['content']

def process_policy_files(input_folder, output_folder):
    """
    Reads DeepSeek output files, sends them to GPT, and saves structured results.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Samples for the one-shot, deepseek sample text, gpt-style expected output
    with open("../Output/deepseek/textResults/2shot/584_communitycoffee.com_result.txt", "r", encoding="utf-8") as file:
        deepseek_output = file.read()
    with open("../Output/gpt35_turbo/textResults/2shot/584_communitycoffee.com_result.txt", "r", encoding="utf-8") as file:
        expected_output = file.read()

    for filename in os.listdir(input_folder):
        if filename.endswith("_result.txt"):  
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r", encoding="utf-8") as file:
                policy_text = file.read()

            formatted_output = reformat_categories_with_gpt(policy_text, deepseek_output=deepseek_output, expected_output=expected_output)

            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(formatted_output + "\n")

            print(f"Processed: {filename} -> {output_path}")

# Example usage
input_folder = "../Output/deepseek/textResults/1shot"  # Change this to the correct input path
output_folder = "../Output/deepseek/newTextResults/1shot"  # Change this to the desired output path

process_policy_files(input_folder, output_folder)