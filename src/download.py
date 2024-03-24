import os
import pandas as pd
from urllib import request
import fitz  # PyMuPDF
import re
import time
import sys
import json


def download_pdf(url: str, pdf_file_name: str) -> str:
    """Download PDF from given URL to local directory using proxy."""
    try:


        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = request.Request(url, headers=headers)
        with request.urlopen(req) as response:
            if response.status == 200:
                filepath = os.path.join(os.getcwd(), pdf_file_name)
                with open(filepath, 'wb') as pdf_object:
                    pdf_object.write(response.read())
                print(f'{pdf_file_name} was successfully saved!')
                return filepath  # Return the path to the downloaded PDF file
            else:
                print(f'Uh oh! Could not download {pdf_file_name}, HTTP response status code: {response.status}')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return None

def extract_phone_numbers_from_pdf(pdf_path: str):
    # Regular expression pattern for matching phone numbers with country code and optional spaces
    phone_pattern = r'\+\d{1,3}(?:\s*\d+)+'
    phone_numbers = set()

    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        phone_numbers.update(re.findall(phone_pattern, text))

    return phone_numbers

def extract_emails_from_pdf(pdf_path: str):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = {"CB_email": set(), "Department_email": set()}  

    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        if "Information on the Certification Body" in text:
            emails["CB_email"].update(re.findall(email_pattern, text))
        elif "System User and Audit Process" in text:
            emails["Department_email"].update(re.findall(email_pattern, text))

    return emails

if __name__ == '__main__':
    folder_path = "table"  

    dfo = pd.read_csv(os.path.join("DB"),'ALL_Clean_DB.csv')
    num_rows, _ = dfo.shape



    df = pd.read_csv(os.path.join(folder_path),"clean_data_240.csv")


    request_count = 0

    for index, row in dfo.iterrows():
            url = row['Audit Report']   
            file_name = f"temp_{index}.pdf"

            if request_count == 45:

                request_count = 0  

            pdf_path = download_pdf(url, file_name)


            if pdf_path:
                phone_numbers = extract_phone_numbers_from_pdf(pdf_path)
                emails = extract_emails_from_pdf(pdf_path)
                
                df['Phone Numbers'][index] = phone_numbers
                df['Emails'][index] = emails
                os.remove(pdf_path)
            else:
                df['Phone Numbers'][index] = "N/A"
                df['Emails'][index] = "N/A"

            csv_file_path = os.path.join(folder_path, f"clean_csv_{index}.csv")
            df.to_csv(csv_file_path, index=False)

            request_count += 1

    print("Program finished!")