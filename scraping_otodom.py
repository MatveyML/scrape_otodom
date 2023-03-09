from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

t0 = time.time()
all_hrefs = []
#driver settings
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(r"C:\Users\User\Documents\Python\chromedriver_win32\chromedriver.exe",options=options)

url = 'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/warszawa?page=1'
driver.get(url)
# parse the HTML content
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
#find the number of pages
last_page = soup.find(class_="css-1ohxh6y eoupkm70").findNextSibling(class_="eoupkm71 css-190hi89 e11e36i3").text
last_page = int(last_page)
print('amount of pages:',last_page)
for i in range(1, last_page+1):

    url = f'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/warszawa?page={i}'
    driver.get(url)

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #press 'accept' botton if appears
    try:
        accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click()
    except NoSuchElementException:
        pass

    # parse the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # extract the hrefs
    flat_links = soup.find_all(attrs={'data-cy': 'listing-item-link'})
    for link in flat_links:
        href = 'https://www.otodom.pl/' + link.get('href')
        all_hrefs.append(href)
print('Amount of appartments: ', len(all_hrefs))

price_list = []
address_list = []
czynsz_list = []
pow_list = []
rooms_list = []
zabud_list = []
who_list = []
name_list = []

for i, href in enumerate(all_hrefs):
    print(f'{i}){href}')
    driver.get(href)
    #press 'accept' button if appears
    try:
        accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click()
    except NoSuchElementException:
        pass
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        # wait until certain element appears in the html (ad banner at the bottom of the page)
        wait = WebDriverWait(driver, 30)  # Set the timeout to 20 seconds
        last_el_need = wait.until(EC.presence_of_element_located((By.ID, "map")))
    except:
        pass
    # parse the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #name
    try:
        name = soup.find('h1',class_="css-1sfzh0a eu6swcv20").text.strip()
        name_list.append(name)
        #price
        price = soup.find("strong",{"aria-label":"Cena"}).text.strip()
        price_list.append(price)
        #address
        address = soup.find(class_="e1nbpvi60 css-171pgf6 e1enecw71").text.strip()
        address_list.append(address)

    #czynsz
        try:
            czynsz = soup.find("div", {"aria-label": "Czynsz"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-1wi2w6s estckra5").text.strip()
            czynsz_list.append(czynsz)
        except:
            czynsz = soup.find("div", {"aria-label": "Czynsz"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_='css-lux9hg ekf916v1').text.strip()
            czynsz_list.append(czynsz)
        #powierzchnia
        try:
            pow = soup.find("div", {"aria-label": "Powierzchnia"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-1wi2w6s estckra5").text.strip()
            pow_list.append(pow)
        except:
            pow = soup.find("div", {"aria-label": "Powierzchnia"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-lux9hg ekf916v1").text.strip()
            pow_list.append(pow)
        #liczba pokoi
        try:
            rooms = soup.find("div", {"aria-label": "Liczba pokoi"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-1wi2w6s estckra5").text.strip()
            rooms_list.append(rooms)
        except:#none starts from small n, not N
            rooms = soup.find("div", {"aria-label": "Liczba pokoi"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-lux9hg ekf916v1").text.strip()
            rooms_list.append(rooms)
        #Rodzaj zabudowy
        try:
            zabud = soup.find("div", {"aria-label": "Rodzaj zabudowy"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-1wi2w6s estckra5").text.strip()
            zabud_list.append(zabud)
        except:
            zabud = soup.find("div", {"aria-label": "Rodzaj zabudowy"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-lux9hg ekf916v1").text.strip()
            zabud_list.append(zabud)
        #Typ ogłoszeniodawcy
        try:
            who = soup.find("div", {"aria-label": "Typ ogłoszeniodawcy"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-1wi2w6s estckra5").text.strip()
            who_list.append(who)
        except:
            who = soup.find("div", {"aria-label": "Typ ogłoszeniodawcy"}).findChild(class_="css-1qzszy5 estckra8").findNext(
                class_="css-1qzszy5 estckra8").findChild(class_="css-lux9hg ekf916v1").text.strip()
            who_list.append(who)
    except AttributeError:
        pass
#correct address list
words_to_remove = ['Warszawa, ',', Warszawa',' Warszawa,',', mazowieckie']
new_address_list = []
for address in address_list:
    for word in words_to_remove:
        address = address.replace(word,'')
    new_address_list.append(address)
district_list = []
street_list = []
for location in new_address_list:
    if ',' in location:
        district, street = location.split(', ', 1)
        district_list.append(district)
        street_list.append(street)
    else:
        district_list.append(location)
        street_list.append(None)
#correct price list
new_price_list = []
for price in price_list:
    price = price.replace(' zł','')
    new_price_list.append(price)
#correct czynsz list
new_czynsz_list = []
for czynsz in czynsz_list:
    if czynsz == 'Zapytaj':
        czynsz = 0
    else:
        czynsz = czynsz.replace(' zł/miesiąc','')
    new_czynsz_list.append(czynsz)
#correct area
new_area_list = []
for pow in pow_list:
    pow = pow.replace(' m²','')
    new_area_list.append(pow)
print(
name_list,'amount of elements',len(name_list),
"\n",price_list,'amount of elements',len(price_list),
"\n",address_list,'amount of elements',len(address_list),
"\n",czynsz_list,'amount of elements',len(czynsz_list),
"\n",pow_list,'amount of elements',len(pow_list),
"\n",rooms_list,'amount of elements',len(rooms_list),
"\n",zabud_list,'amount of elements',len(zabud_list),
"\n",who_list,'amount of elements',len(who_list)
      )

# close the browser
driver.close()

data = {
    'Name':name_list,
    'Price':new_price_list,
    'District':district_list,
    'Street':street_list,
    'Czynsz':new_czynsz_list,
    'Area':new_area_list,
    'Rooms':rooms_list,
    'Building':zabud_list,
    'Owner':who_list
}
df = pd.DataFrame(data)
df.to_csv('otodom_scrap.csv',index=False)
t1 = time.time()
print('Running',t1-t0,'sec')

