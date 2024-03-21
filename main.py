import os
import requests
import PyPDF2
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from pdf_scrap import extract_emails_from_pdf,download_pdf_file,extract_phone_numbers_from_pdf

def scrape_certificates(link: str, num_pages: int):
    """Scrape certificate data from a website."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920, 1080")
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get(link)

    for i in range(1, num_pages + 1):
        certificates_data = []
        page_number = str(format(i, ","))
        WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.LINK_TEXT, page_number)))
        next_table = driver.find_element(By.LINK_TEXT, f"{page_number}")
        next_table.click()
        table_body = driver.find_element(By.XPATH, "//tbody")
        table_body_html = table_body.get_attribute("innerHTML")
        soup = BeautifulSoup(table_body_html, 'html.parser')
        rows = soup.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            certificate = {}
            if len(cells) > 7:
                certificate['Status'] = cells[0].find('span', class_='has-tip')['title'] if cells[0].find('span', class_='has-tip') is not None else 'N/A'
                certificate['Certificate ID'] = cells[1].text.strip()
                certificate['Certificate Holder'] = cells[2].text.strip()
                certificate['Scope'] = cells[3].text.strip() if cells[3].text.strip() else 'N/A'
                certificate['Raw Material'] = cells[4].text.strip() if cells[4].text.strip() else 'N/A'
                certificate['Add-Ons'] = cells[5].text.strip() if cells[5].text.strip() else 'N/A'
                certificate['Products'] = cells[6].text.strip() if cells[6].text.strip() else 'N/A'
                certificate['Valid From'] = cells[7].text.strip() if cells[7].text.strip() else 'N/A'
                certificate['Valid Until'] = cells[8].text.strip() if cells[8].text.strip() else 'N/A'
                certificate['Suspended'] = cells[9].text.strip() if cells[9].text.strip() else 'N/A'
                certificate['Issuing CB'] = cells[10].text.strip() if cells[10].text.strip() else 'N/A'
                certificate['Map'] = cells[11].find('a')['href'] if cells[11].find('a') is not None else ''
                certificate['Certificate'] = cells[12].find('a')['href'] if cells[12].find('a') is not None else ''
                cert_aduit_url = cells[13].find('a')['href'] if cells[13].find('a') is not None else ''
                certificate['Audit Report'] = cert_aduit_url
                pdf_path = "temp.pdf"
                download_pdf_file(cert_aduit_url, pdf_path)
                found_emails = extract_emails_from_pdf(pdf_path)
                certificate['Emails'] = list(found_emails) if found_emails else []
                found_phone_numbers = extract_phone_numbers_from_pdf(pdf_path)
                certificate['Phone Numbers'] = list(found_phone_numbers) if found_phone_numbers else []

                os.remove(pdf_path)
            else:
                certificate['Status'] = ''
                certificate['Certificate ID'] = cells[1].text.strip()
                certificate['Certificate Holder'] = cells[2].text.strip()
                certificate['Map'] = cells[3].find('a')['href'] if cells[3].find('a') is not None else ''
                certificate['Certificate'] = cells[4].find('a')['href'] if cells[4].find('a') is not None else ''
                cert_aduit_url = cells[5].find('a')['href'] if cells[5].find('a') is not None else ''
                certificate['Audit Report'] = cert_aduit_url
                pdf_path = "temp.pdf"
                download_pdf_file(cert_aduit_url, pdf_path)
                found_emails = extract_emails_from_pdf(pdf_path)
                certificate['Emails'] = list(found_emails) if found_emails else []
                os.remove(pdf_path)
                certificate['Scope'] = ''
                certificate['Raw Material'] = ''
                certificate['Add-Ons'] = ''
                certificate['Products'] = ''
                certificate['Valid From'] = ''
                certificate['Valid Until'] = ''
                certificate['Suspended'] = ''
                certificate['Issuing CB'] = ''
            certificates_data.append(certificate)

        df = pd.DataFrame(certificates_data)
        df.to_csv(f'Full_certificate_DataBase_{i}.csv', index=False)
    print("Scraping Completed")
    driver.close()

if __name__ == "__main__":
    link = "https://www.iscc-system.org/certification/certificate-database/all-certificates/"
    num_pages = 2  # Change this to the actual number of pages
    scrape_certificates(link, num_pages)
