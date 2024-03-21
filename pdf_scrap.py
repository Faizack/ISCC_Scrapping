import os
import requests
import PyPDF2
import re


def download_pdf_file(url: str, pdf_file_name: str) -> bool:
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False


def extract_emails_from_pdf(pdf_path: str):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    emails = set()
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            emails.update(re.findall(email_pattern, text))

    return emails


def extract_phone_numbers_from_pdf(pdf_path: str):
    # Regular expression pattern for matching phone numbers with country code and optional spaces
    phone_pattern = r'\+\d{1,3}(?:\s*\d+)+'

    phone_numbers = set()
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            phone_numbers.update(re.findall(phone_pattern, text))

    return phone_numbers


if __name__ == '__main__':
    # URL from which pdfs to be downloaded
    URL = 'https://hub.iscc-system.org//FileHandler/download/summaryAuditReportFile/NDQwNzNfRVUtSVNDQy1DZXJ0LURLMjIwLTg4ODcyMDI0'
    pdf_path = "temp.pdf"
    download_pdf_file(URL, pdf_path)

    # Extract emails from PDF
    email_list = []
    found_emails = extract_emails_from_pdf(pdf_path)
    if found_emails:
        print("Email addresses found in the PDF:")
        for email in found_emails:
            email_list.append(email)
        print(email_list)
    else:
        print("No email addresses found in the PDF.")

    # Extract phone numbers from PDF
    phone_list = []
    found_phone_numbers = extract_phone_numbers_from_pdf(pdf_path)
    if found_phone_numbers:
        print("\nPhone numbers found in the PDF:")
        for phone_number in found_phone_numbers:
            phone_list.append(phone_number)
        print(phone_list)
    else:
        print("\nNo phone numbers found in the PDF.")

    # Remove the downloaded PDF file
    os.remove(pdf_path)
