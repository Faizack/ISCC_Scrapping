import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from pdf_scrap import extract_emails_from_pdf,download_pdf_file,extract_phone_numbers_from_pdf

import os
import pandas as pd

def scrape_certificates(link: str, num_pages: int):
    """Scrape certificate data from a website."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920, 1080")
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get(link)

    # Initialize lists for each column
    status_column = []
    id_column = []
    holder_column = []
    scope_column = []
    raw_material_column = []
    add_ons_column = []
    products_column = []
    valid_from_column = []
    valid_until_column = []
    suspended_column = []
    issuing_cb_column = []
    map_column = []
    certificate_column = []
    audit_report_column = []

    for i in range(1, num_pages + 1):
        page_number = str(format(i, ","))
        print(page_number)
        WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.LINK_TEXT, page_number)))
        next_table = driver.find_element(By.LINK_TEXT, f"{page_number}")
        next_table.click()
        table_body = driver.find_element(By.XPATH, "//tbody")
        table_body_html = table_body.get_attribute("innerHTML")
        soup = BeautifulSoup(table_body_html, 'html.parser')
        rows = soup.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells)== 15:
                status_column.append(cells[0].find('span', class_='has-tip')['title'] if cells[0].find('span', class_='has-tip') is not None else 'N/A')
                id_column.append(cells[1].text.strip())
                holder_column.append(cells[2].text.strip())
                scope_column.append(cells[3].text.strip() if cells[3].text.strip() else 'N/A')
                raw_material_column.append(cells[4].text.strip() if cells[4].text.strip() else 'N/A')
                add_ons_column.append(cells[5].text.strip() if cells[5].text.strip() else 'N/A')
                products_column.append(cells[6].text.strip() if cells[6].text.strip() else 'N/A')
                valid_from_column.append(cells[7].text.strip() if cells[7].text.strip() else 'N/A')
                valid_until_column.append(cells[8].text.strip() if cells[8].text.strip() else 'N/A')
                suspended_column.append(cells[9].text.strip() if cells[9].text.strip() else 'N/A')
                issuing_cb_column.append(cells[10].text.strip() if cells[10].text.strip() else 'N/A')
                map_column.append(cells[11].find('a')['href'] if cells[11].find('a') is not None else '')
                certificate_column.append(cells[12].find('a')['href'] if cells[12].find('a') is not None else '')
                audit_report_column.append(cells[13].find('a')['href'] if cells[13].find('a') is not None else '')



        # Create DataFrame from the collected columns
        df = pd.DataFrame({
            "Status": status_column,
            "Certificate ID": id_column,
            "Certificate Holder": holder_column,
            "Scope": scope_column,
            "Raw Material": raw_material_column,
            "Add-Ons": add_ons_column,
            "Products": products_column,
            "Valid From": valid_from_column,
            "Valid Until": valid_until_column,
            "Suspended": suspended_column,
            "Issuing CB": issuing_cb_column,
            "Map": map_column,
            "Certificate": certificate_column,
            "Audit Report": audit_report_column
        })

        # Save DataFrame to CSV file
        df.to_csv(f'Full_certificate_DataBase_{i}.csv', index=False)

    print("Scraping Completed")
    driver.close()

if __name__ == "__main__":
    link = "https://www.iscc-system.org/certification/certificate-database/all-certificates/"
    num_pages = 5571  # Change this to the actual number of pages
    scrape_certificates(link, num_pages)
