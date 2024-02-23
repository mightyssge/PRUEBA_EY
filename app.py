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

app = Flask(__name__)

@app.route('/api/entidades/<filtro>',methods=['GET'])
def apientidades(filtro):
    #We check if the filter is empty
    if filtro == '':
        return jsonify({'error': 'No se ha ingresado un filtro'}), 400

    # Set the path to the ChromeDriver executable
    chromedriver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

    # Initialize the Chrome webdriver service with the path to the ChromeDriver executable
    service = Service(executable_path=chromedriver_path)

    # Initialize the Chrome webdriver with the Chrome webdriver service
    driver = webdriver.Chrome(service=service)
    driver.get('https://sanctionssearch.ofac.treas.gov')

    #We setup the name for the filter
    

    #We find the input field and send the filter and also we click the submit button to get all the data
    input_field = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$txtLastName"]').send_keys(filtro)
    accept_button = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$btnSearch"]').click()

    # We wait for the search results to appear on the page
    wait = WebDriverWait(driver, 10)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table that contains the data we want to scrape
    table = soup.find('table', attrs={'id': 'gvSearchResults'})

    if table is None:
        # No results were found
        driver.quit()
        return jsonify({'error': 'No se encontraron resultados para el filtro ingresado'}), 404


    entities = []
    for row in table:
        cells = row.find_all('td')
        entities.append( [cell.get_text(strip=True) for cell in cells])


    data = [{'Name': entity[0], 'Address': entity[1], 'Type': entity[2], 'Program(s)': entity[3], 'List': entity[4], 'Score': entity[5]} for entity in entities]

    #We close the webdriver
    driver.quit()
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)






