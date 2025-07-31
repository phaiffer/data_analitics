import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urljoin
import re
import time
import pandas as pd
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

KEYWORDS = ['contato', 'fale conosco', 'about', 'about us', 'contact', 'contact us', 'contáctanos']


def get_domain_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def create_email_pattern(domain: str) -> re.Pattern:
    escaped_domain = re.escape(domain)
    pattern_str = rf'[\w\.-]+@([\w\-]+\.)*{escaped_domain}'
    return re.compile(pattern_str, re.IGNORECASE)


def setup_driver(headless: bool = True) -> webdriver.Chrome:
    chromedriver_autoinstaller.install()
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    return driver


def find_emails_on_page(driver: webdriver.Chrome, pattern: re.Pattern) -> set:
    html = driver.page_source
    return set(pattern.findall(html))


def find_contact_links(driver: webdriver.Chrome) -> list:
    links = driver.find_elements(By.TAG_NAME, "a")
    contact_links = []
    for link in links:
        href = link.get_attribute("href")
        text = (link.text or "").lower()
        if href and any(keyword in text for keyword in KEYWORDS):
            contact_links.append(href)
    return contact_links


def scrape_emails_from_site(url: str, headless: bool = True) -> set:
    domain = get_domain_from_url(url)
    email_pattern = create_email_pattern(domain)
    emails_found = set()
    visited_urls = set()

    logging.info(f"Processando site: {url}")

    driver = setup_driver(headless=headless)

    try:
        driver.get(url)
        time.sleep(2)

        emails_found.update(find_emails_on_page(driver, email_pattern))

        # Se já encontrou e-mails na página inicial, evita buscar em links de contato
        if not emails_found:
            contact_links = find_contact_links(driver)

            for link in contact_links:
                full_url = urljoin(url, link)
                if full_url not in visited_urls and domain in full_url:
                    try:
                        driver.get(full_url)
                        time.sleep(2)
                        emails_found.update(find_emails_on_page(driver, email_pattern))
                        visited_urls.add(full_url)
                        if emails_found:
                            break
                    except Exception as e:
                        logging.warning(f"Falha ao acessar {full_url}: {e}")

    except Exception as e:
        logging.error(f"Erro ao acessar {url}: {e}")
    finally:
        driver.quit()

    return emails_found


def load_sites_from_csv(filepath: str) -> list:
    df = pd.read_csv(filepath)
    return df['url'].dropna().tolist()


def save_results(emails_dict: dict, emails_file: str, no_email_file: str) -> None:
    rows = []
    no_email_sites = []

    for site, emails in emails_dict.items():
        if emails:
            for email in sorted(emails):
                rows.append({"URL": site, "Email": email})
        else:
            no_email_sites.append(site)

    df_emails = pd.DataFrame(rows)
    df_emails.to_csv(emails_file, index=False)

    if no_email_sites:
        df_no_email = pd.DataFrame(no_email_sites, columns=["URL"])
        df_no_email.to_csv(no_email_file, index=False)


def main():
    sites_file = "links.csv"
    emails_output = "emails_encontrados.csv"
    no_emails_output = "sem_email.csv"

    sites = load_sites_from_csv(sites_file)
    all_emails = {}

    for site in sites:
        emails = scrape_emails_from_site(site, headless=True)
        all_emails[site] = emails

    save_results(all_emails, emails_output, no_emails_output)
    logging.info(f"Processo finalizado. Resultados salvos em '{emails_output}' e '{no_emails_output}'.")


if __name__ == "__main__":
    main()
