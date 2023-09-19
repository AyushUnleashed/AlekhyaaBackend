import PyPDF2
import re

def pdf_to_text_with_links(pdf_path, output_text_file):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize variables to store text and links
        pdf_text = ""
        links = []

        # Loop through each page in the PDF
        for page_num in range( len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

        # Use regular expressions to find links in the text
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(link_pattern, pdf_text)

        # Save the text to a text file
        with open(output_text_file, 'w', encoding='utf-8') as text_file:
            text_file.write(pdf_text)

        return links

if __name__ == "__main__":
    # Example usage
    pdf_path = 'pib.pdf'  # Replace with your PDF file path
    output_text_file = 'output.txt'  # Replace with the desired output text file name

    extracted_links = pdf_to_text_with_links(pdf_path, output_text_file)

    # Print the extracted links
    print("Extracted links:")
    for link in extracted_links:
        print(link)