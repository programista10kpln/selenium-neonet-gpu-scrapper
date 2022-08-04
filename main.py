from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def search_elements_by_css_selector(selector: str, timeout: int = 30):
    return WebDriverWait(driver, timeout=timeout).until(lambda d: d.find_elements(By.CSS_SELECTOR, selector))


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
neonet_url = r'https://www.neonet.pl/podzespoly-komputerowe/karty-graficzne.html'
driver.get(neonet_url)

driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

names = [el.text.strip() for el in search_elements_by_css_selector(
    '.listingItemCss-nameLink-1rv')]
attrs = [el.text.strip().split('\n') for el in search_elements_by_css_selector(
    '.productAttributesCss-attributes__group-q5V')]
attrs_dicts = []
for item in attrs:
    dct = {item[i].replace(':', ''): item[i + 1]
           for i in range(0, len(item), 2)}
    attrs_dicts.append(dct)
prices = [el.text.strip().replace(',', '.')
          for el in search_elements_by_css_selector('.uiPriceCss-price-3nF')]
hrefs = [el.get_attribute("href") for el in search_elements_by_css_selector(
    '.listingItemCss-nameLink-1rv')]


gpus = []


if len(names) == len(prices):
    for i in range(0, len(names)):
        gpu_dict = {}

        gpu_dict['nazwa'] = names[i]
        gpu_dict.update(attrs_dicts[i])
        gpu_dict['cena'] = prices[i]
        gpu_dict['hiperłącze'] = hrefs[i]

        gpus.append(gpu_dict)
else:
    print('error: data length is not matched')


for gpu in gpus:
    print(gpu, '\n')


driver.quit()
