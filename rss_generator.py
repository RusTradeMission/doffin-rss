import time
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def generate_rss():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    url = "https://www.doffin.no/search?type=DYNAMIC_PURCHASING_SCHEME"
    driver.get(url)
    time.sleep(5)

    notices = driver.find_elements(By.CSS_SELECTOR, 'a.notice-title-link')

    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = "Doffin – Dynamic Purchasing Schemes"
    SubElement(channel, 'link').text = url
    SubElement(channel, 'description').text = "Latest dynamic purchasing schemes from Doffin.no"
    SubElement(channel, 'language').text = "en"
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0100')

    for notice in notices[:10]:
        link = notice.get_attribute('href')
        title = notice.text.strip()
        parent = notice.find_element(By.XPATH, '../../..')
        pub_date_elem = parent.find_element(By.CSS_SELECTOR, '.published-date')
        pub_date_str = pub_date_elem.text.strip()
        pub_date = datetime.strptime(pub_date_str, "%d.%m.%Y")

        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = title
        SubElement(item, 'link').text = link
        SubElement(item, 'guid').text = link
        SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y 00:00:00 +0100')
        SubElement(item, 'description').text = f"<![CDATA[{title} – published {pub_date_str}.]]>"

    tree = ElementTree(rss)
    tree.write("docs/feed.xml", encoding="utf-8", xml_declaration=True)
    driver.quit()

if __name__ == "__main__":
    generate_rss()
