# Certificate Scraper

This Python script scrapes certificate data from a website, extracts information including certificate ID, certificate holder, scope, raw material, add-ons, products, validity period, and more. It also downloads associated PDF files containing audit reports and extracts email addresses from them.

## Requirements

- Python 3.12.2

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Download the Chrome Web Driver appropriate for your operating system from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

1. Clone this repository or download the `certificate_scraper.py` file.
2. Ensure all dependencies are installed and the Chrome Web Driver is available in your system PATH.
3. Modify the `link` variable in the script to specify the URL of the website you want to scrape.
4. Modify the `num_pages` variable to set the number of pages you want to scrape.
5. Run the script:

```bash
python main.py
```

The script will scrape the specified number of pages, save certificate data as CSV files (`Full_certificate_DataBase_<page_number>.csv`), and download associated PDF files with audit reports.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request with any improvements or fixes.

