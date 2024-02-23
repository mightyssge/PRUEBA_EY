import requests
import os
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selectolax.parser import HTMLParser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import Flask,jsonify




#We first setup de webdriver and go to the website
service = Service(executable_path=r"C:\Users\Alvaro\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://sanctionssearch.ofac.treas.gov')


#We setup the name for the filter
filtro = "usa"

#We find the input field and send the filter and also we click the submit button to get all the data
input_field = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$txtLastName"]').send_keys(filtro)
accept_button = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$btnSearch"]').click()

# We wait for the search results to appear on the page
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@id="resultsHeaderTable"]')))

# We parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')


#The next code serves to print the whole HTML content of the page in a format that is easier to read
'''
# We get the formatted HTML content of the page
formatted_html = soup.prettify()

# We split the formatted HTML content into smaller chunks
chunk_size = 1000
formatted_html_chunks = [formatted_html[i:i + chunk_size] for i in range(0, len(formatted_html), chunk_size)]

# We print each chunk of the formatted HTML content separately
for chunk in formatted_html_chunks:
    print(chunk)
'''

#We find the table that contains the data we want to scrape
table = soup.find('table', attrs={'id': 'gvSearchResults'}).find('tbody').find_all('tr')

entities = []
for row in table:
    cells = row.find_all('td')
    entities.append( [cell.get_text(strip=True) for cell in cells])


data = [{'Name': entity[0], 'Address': entity[1], 'Type': entity[2], 'Program(s)': entity[3], 'List': entity[4], 'Score': entity[5]} for entity in entities]

json_data = json.dumps(data, indent=4)

with open('entidades.json', 'w') as json_file:
    json_file.write(json_data)

driver.quit()


app = Flask(__name__)

@app.route('/apientidades',methods=['GET'])
def apientidades():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")





