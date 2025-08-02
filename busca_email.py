import re
import time
import pandas as pd
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

df_links = pd.read_csv("links.csv", header=None, names=["URL"])
df_links = df_links[df_links["URL"].str.startswith("http")].reset_index(drop=True)

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def extract_emails_from_site(url):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        emails = list(set(re.findall(EMAIL_REGEX, body_text)))
        driver.quit()
        return emails if emails else [""]
    except Exception as e:
        print(f"Error: {url} -> {e}")
        return [""]

results = []
for url in df_links["URL"]:
    print(f"Processing: {url}")
    emails = extract_emails_from_site(url)
    company = urlparse(url).netloc.replace("www.", "").split(".")[0]
    results.append({
        "Company": company,
        "URL": url,
        "Emails": ", ".join(emails)
    })

df_result = pd.DataFrame(results)
df_result.to_csv("emails_extracted.csv", index=False)
print("Done! File saved as emails_extracted.csv")
