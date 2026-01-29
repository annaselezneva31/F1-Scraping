from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import os

RACE_URL = "https://www.formula1.com/en/results/2025/races"
PATH = os.environ.get("PATH")

def process_string(race_year, race_date, race_name, a):
    a = a.split("\n")
    total = [race_year, race_date, race_name]
    for el in a:
        if el == a[0] or el == a[-1]:
            b = el.split(" ")
            for i in b:
                total.append(i)
        else:
            total.append(el)
    return total


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(PATH)

driver = webdriver.Chrome(options=chrome_options)
driver.get(RACE_URL)

race_years = WebDriverWait(driver, 2).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'menu[aria-labelledby="seasons-dropdown"]')))
list_years = race_years.find_elements(By.TAG_NAME, "a")
href_years = [element.get_attribute('href') for element in list_years]
num_years = [element.split("/")[-2] for element in href_years]
print(href_years)
print(num_years)

total_races = [["year", "date", "race_name", "pos", "num_driver", "driver", "team", "laps", "time", "points"]]

for year in href_years[:3]:
    year_index = href_years.index(year)
    driver.get(year)
    tabel_grand_prix = WebDriverWait(driver, 2).until(ec.presence_of_element_located((By.ID, "results-table")))
    list_grand_prix = tabel_grand_prix.find_elements(By.TAG_NAME, "a")
    href_grand_prix = [element.get_attribute('href') for element in list_grand_prix]
    name_grand_prix = [element.text for element in list_grand_prix]
    list_date = tabel_grand_prix.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(2)')
    date_grand_prix = [element.text for element in list_date]
    print(href_grand_prix)
    print(name_grand_prix)
    for race in href_grand_prix:
        race_index = href_grand_prix.index(race)
        driver.get(race)
        results = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
        race_result = [element.text for element in results]
        for element in race_result:
            total_races.append(process_string(num_years[year_index], date_grand_prix[race_index], name_grand_prix[race_index], element))

print(total_races)

with open("example_of_result.csv", "a", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(total_races)
