import requests
import os

def query_gpt_with_policies(api_url, api_key, html_folder, categories_folder, output_folder, gpt_response_file):
    """
    Parses policies, combines with extracted categories, queries GPT-4 Mini using the given prompt structure, and saves responses.

    Args:
        api_url (str): URL for the GPT-4 Mini API endpoint.
        api_key (str): API key for authentication.
        html_folder (str): Folder containing HTML policy files.
        categories_folder (str): Folder containing category text files.
        output_folder (str): Folder to save sanitized policy texts.
        gpt_response_file (str): Path to save GPT responses.
    """
    def html_to_txt(input_html_path):
        """
        Converts HTML to plain text.
        """
        from bs4 import BeautifulSoup

        try:
            with open(input_html_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            plain_text = soup.get_text(separator="\n", strip=True)

            return plain_text
        except Exception as e:
            print(f"Error parsing HTML file {input_html_path}: {e}")
            return None

    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Prepare to store GPT responses
        gpt_responses = []

        # Process each policy
        for file_name in os.listdir(html_folder):
            if file_name.endswith(".html"):
                # Parse HTML to plain text
                html_path = os.path.join(html_folder, file_name)
                policy_text = html_to_txt(html_path)
                if not policy_text:
                    continue

                # Load corresponding categories
                category_file = os.path.join(categories_folder, f"{os.path.splitext(file_name)[0]}.txt")
                if os.path.exists(category_file):
                    with open(category_file, 'r', encoding='utf-8') as cat_file:
                        policy_categories = cat_file.read().strip()
                else:
                    print(f"Category file not found for {file_name}, skipping.")
                    continue

                # Prepare the prompt using the provided structure
                prompt = f"""
Let's think step by step.

In the privacy policy:
"{policy_text}"

you have identified with "Yes" the present categories:
"{policy_categories}"

For only the present category, locate where it is discussed in the policy and evaluate the sentiment based on the following steps:
- Step 1: Identify the relevant section of the text for this category.
- Step 2: Analyze whether the text suggests a user-friendly or user-risky practice.
- Step 3: Conclude with a sentiment classification for this category (e.g., Positive, Neutral, Negative) and explain why.

In the answer, provide only the final sentiment analysis for each category in the following format:  
Category Name: Sentiment (e.g. Positive, Neutral, Negative) - [Brief Explanation]
"""

                # Query GPT-4 Mini
                response = requests.post(
                    api_url,
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": "gpt-4-mini", "prompt": prompt, "max_tokens": 1000}
                )

                if response.status_code == 200:
                    gpt_responses.append({
                        "policy": file_name,
                        "categories": policy_categories,
                        "response": response.json().get("choices", [{}])[0].get("text", "").strip()
                    })
                else:
                    print(f"Error querying GPT for {file_name}: {response.status_code}, {response.text}")

        # Save GPT responses to file
        with open(gpt_response_file, 'w', encoding='utf-8') as f:
            for entry in gpt_responses:
                f.write(f"Policy: {entry['policy']}\n")
                f.write(f"Categories:\n{entry['categories']}\n")
                f.write(f"GPT-4 Mini Response:\n{entry['response']}\n")
                f.write("-" * 80 + "\n")

        print(f"GPT responses saved to: {gpt_response_file}")

    except Exception as e:
        print(f"Error: {e}")

# Example Usage
if __name__ == "__main__":
    api_url = "https://api.openai.com/v1/completions"  # Replace with GPT-4 Mini API endpoint
    api_key = "../api_key.txt"  # Replace with your API key
    html_folder = "sanitized_policies"  # Folder containing HTML policy files
    categories_folder = "categories_texts"  # Folder containing category text files
    output_folder = "sanitized_texts"  # Folder to save parsed text files
    gpt_response_file = "gpt_policy_analysis.txt"  # File to save GPT responses

    query_gpt_with_policies(api_url, api_key, html_folder, categories_folder, output_folder, gpt_response_file)