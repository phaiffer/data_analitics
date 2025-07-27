import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

df_urls = pd.read_csv('startups.csv')

resultados = []

for url in df_urls['url']:
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class^="headlines__H1"]'))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        names = soup.select('[class^="headlines__H1"]')
        description = soup.select('[class^="ProfileDetails__ProfileDetailsContent"] > div')
        country_segment_elements = soup.select('[class^="ContentTagList__ContentTagListItem"]')
        social_blocks = soup.select('[class^="DetailsLayout__SocialMediaWrapper"]')
        buttons = soup.select('[class^="Button__StyledButton"]')

        descriptions = description[0].get_text(strip=True) if description else ""
        country = country_segment_elements[0].get_text(strip=True) if len(country_segment_elements) > 0 else ""
        segment = country_segment_elements[1].get_text(strip=True) if len(country_segment_elements) > 1 else ""

        instagram = ""
        linkedin = ""

        for block in social_blocks:
            links = block.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'instagram.com' in href:
                    instagram = href
                elif 'linkedin.com' in href:
                    linkedin = href

        href_buttons = [btn['href'] for btn in buttons if btn.has_attr('href')]
        web_site = href_buttons[2] if len(href_buttons) >= 3 else ""

        profile = {
            "url": url,
            "name": names[0].get_text(strip=True) if names else "",
            "description": descriptions,
            "country": country,
            "segment": segment,
            "instagram": instagram,
            "linkedin": linkedin,
            "web_site": web_site
        }

        resultados.append(profile)

    except Exception as e:
        print(f"Erro ao processar {url}: {e}")

driver.quit()

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('perfis_extraidos.csv', index=False, encoding='utf-8')
print("Extração finalizada e salva em 'perfis_extraidos.xlsx'")
