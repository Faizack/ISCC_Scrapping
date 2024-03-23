import os
import pandas as pd
from urllib import request
import fitz  # PyMuPDF
import re

def download_pdf_file(url: str, pdf_file_name: str) -> bool:
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """
    try:
        with request.urlopen(url) as response:
            if response.status == 200:
                filepath = os.path.join(os.getcwd(), pdf_file_name)
                with open(filepath, 'wb') as pdf_object:
                    pdf_object.write(response.read())
                    print(f'{pdf_file_name} was successfully saved!')
                    return filepath  # Return the path to the downloaded PDF file
            else:
                print(f'Uh oh! Could not download {pdf_file_name},')
                print(f'HTTP response status code: {response.status}')
                return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def extract_countries_from_pdf(pdf_path: str):
    country_pattern = r'\b(?:Afghanistan|Albania|Algeria|Andorra|Angola|Antigua and Barbuda|Argentina|Armenia|Australia|Austria|Azerbaijan|Bahamas|Bahrain|Bangladesh|Barbados|Belarus|Belgium|Belize|Benin|Bhutan|Bolivia|Bosnia and Herzegovina|Botswana|Brazil|Brunei|Bulgaria|Burkina Faso|Burundi|Cabo Verde|Cambodia|Cameroon|Canada|Central African Republic|Chad|Chile|China|Colombia|Comoros|Congo|Costa Rica|Croatia|Cuba|Cyprus|Czech Republic|Democratic Republic of the Congo|Denmark|Djibouti|Dominica|Dominican Republic|East Timor|Ecuador|Egypt|El Salvador|Equatorial Guinea|Eritrea|Estonia|Eswatini|Ethiopia|Fiji|Finland|France|Gabon|Gambia|Georgia|Germany|Ghana|Greece|Grenada|Guatemala|Guinea|Guinea-Bissau|Guyana|Haiti|Honduras|Hungary|Iceland|India|Indonesia|Iran|Iraq|Ireland|Israel|Italy|Ivory Coast|Jamaica|Japan|Jordan|Kazakhstan|Kenya|Kiribati|Kosovo|Kuwait|Kyrgyzstan|Laos|Latvia|Lebanon|Lesotho|Liberia|Libya|Liechtenstein|Lithuania|Luxembourg|Madagascar|Malawi|Malaysia|Maldives|Mali|Malta|Marshall Islands|Mauritania|Mauritius|Mexico|Micronesia|Moldova|Monaco|Mongolia|Montenegro|Morocco|Mozambique|Myanmar|Namibia|Nauru|Nepal|Netherlands|New Zealand|Nicaragua|Niger|Nigeria|North Korea|North Macedonia|Norway|Oman|Pakistan|Palau|Palestine|Panama|Papua New Guinea|Paraguay|Peru|Philippines|Poland|Portugal|Qatar|Romania|Russia|Rwanda|Saint Kitts and Nevis|Saint Lucia|Saint Vincent and the Grenadines|Samoa|San Marino|Sao Tome and Principe|Saudi Arabia|Senegal|Serbia|Seychelles|Sierra Leone|Singapore|Slovakia|Slovenia|Solomon Islands|Somalia|South Africa|South Korea|South Sudan|Spain|Sri Lanka|Sudan|Suriname|Sweden|Switzerland|Syria|Taiwan|Tajikistan|Tanzania|Thailand|Togo|Tonga|Trinidad and Tobago|Tunisia|Turkey|Turkmenistan|Tuvalu|Uganda|Ukraine|United Arab Emirates|United Kingdom|United States|Uruguay|Uzbekistan|Vanuatu|Vatican City|Venezuela|Vietnam|Yemen|Zambia|Zimbabwe)\b'
    countries = set()

    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()

        matches = re.findall(country_pattern, text, flags=re.IGNORECASE)
        if matches:
            countries.update(matches)

    return countries

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
import time

if __name__ == '__main__':
    df = pd.read_csv('clean_data.csv')
    emails_list = [None] * len(df)  
    countries_list = [None] * len(df)  
    phone_numbers_list = [None] * len(df)  

    for index, row in df.iterrows():
        url = row['Audit Report']
        print(url)
        pdf_path = download_pdf_file(url, f"temp_{index}.pdf")

        time.sleep(5)

    print("Program finished !")
