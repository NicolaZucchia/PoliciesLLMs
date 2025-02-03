import os
import openai

# OpenAI API key (ensure you have set it up correctly)
openai.api_key = "...Enter your API key here..."

def reformat_sentiment_with_gpt(policy_text, deepseek_output, expected_output):
    """
    Sends the policy output to GPT for category extraction and formatting.
    """
    prompt = f"""
    You will be given an extracted sentiment analysis from a DeepSeek model analyzing a privacy policy.  
    However, the extracted text is not well formatted and need correction.  

    Your Task is to identify the following steps done by DeepSeek exactly as stated below:
    - Step 1: Identify the relevant section of the text for this category.
    - Step 2: Analyze whether the text suggests a user-friendly or user-risky practice.
    - Step 3: Conclude with a sentiment classification for this category (e.g., Positive, Neutral, Negative) and explain why.

In the answer, provide only the final sentiment analysis in the following format:  
Category Name: Sentiment (e.g., Positive, Neutral, Negative) - [Brief Explanation]"

    - Ensure the sentiment analysis for each category is assigned either "Positive", "Neutral" or "Negative".
    - If multiple mentions exist, take only the last occurrence for each category.
    - You may find alternative words instead of "Positive" and "Negative", it is up to you to understand whether the assign evaluation falls into "Positive", "Neutral" or "Negative".
    - Standardize the output into the following format:

    ```
    Data Category - [Sentiment] - Explanation
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
    with open("deepseekResponses/591_google.com_response.txt", "r", encoding="utf-8") as file:
        deepseek_output = file.read()
    with open("gpt4oResponses/591_google.com_response.txt", "r", encoding="utf-8") as file:
        expected_output = file.read()

    for filename in os.listdir(input_folder):
        if filename.endswith("_response.txt"):  
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r", encoding="utf-8") as file:
                policy_text = file.read()

            formatted_output = reformat_sentiment_with_gpt(policy_text, deepseek_output=deepseek_output, expected_output=expected_output)

            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(formatted_output + "\n")

            print(f"Processed: {filename} -> {output_path}")

# Example usage
input_folder = "deepseekResponses"  # Change this to the correct input path
output_folder = "deepseekNewResponses"  # Change this to the desired output path

process_policy_files(input_folder, output_folder)