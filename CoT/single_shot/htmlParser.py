from bs4 import BeautifulSoup

def html_to_txt(input_html_path, output_txt_path):
    """
    Parse an HTML file and extract the plain text content into a text file.
    
    Args:
        input_html_path (str): Path to the input HTML file.
        output_txt_path (str): Path to save the extracted plain text content.
    """
    try:
        # Read the HTML content from the file
        with open(input_html_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the text content
        plain_text = soup.get_text(separator="\n", strip=True)

        # Write the plain text content to the output file
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(plain_text)

        print(f"Successfully extracted text to: {output_txt_path}")

    except Exception as e:
        print(f"Error while parsing HTML: {e}")

# Example usage
if __name__ == "__main__":
    input_html_path = "20_theatlantic.com.html"  # Replace with your input HTML file path
    output_txt_path = "20_theatlantic.com.txt"   # Replace with your desired output text file path

    html_to_txt(input_html_path, output_txt_path)