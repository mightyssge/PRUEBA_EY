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

from flask import Flask,jsonify,request
from selenium.common.exceptions import TimeoutException


app = Flask(__name__)

@app.route('/api/entidades',methods=['GET'])
def apientidades():

    # Get the "filtro" query parameter
    filtro = request.args.get('query')

    # Check if the filter is empty
    if not filtro:
        return jsonify({'error': 'No se ha ingresado un filtro'}), 400

    # Set the path to the ChromeDriver executable
    chromedriver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

    # Initialize the Chrome webdriver service with the path to the ChromeDriver executable
    service = Service(executable_path=chromedriver_path)

    # Initialize the Chrome webdriver with the Chrome webdriver service
    driver = webdriver.Chrome(service=service)
    driver.get('https://sanctionssearch.ofac.treas.gov')

    # Find the input field and send the filter
    input_field = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$txtLastName"]')
    input_field.send_keys(filtro)

    # Find and click the submit button
    accept_button = driver.find_element(By.XPATH, '//input[@name="ctl00$MainContent$btnSearch"]').click()

    # Wait for the search results to appear on the page
    wait = WebDriverWait(driver, 9)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    found_none = soup.find('span', attrs={'id': '//span[@id="ctl00_MainContent_lblMessage"]'})


    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@id="gvSearchResults"]')))
    except TimeoutException:
        # No results were found
        driver.quit()
        return jsonify({'error': 'No se encontraron resultados para el filtro ingresado'}), 404
        

    # Find the table that contains the data we want to scrape
    table = soup.find('table', attrs={'id': 'gvSearchResults'})

    entities = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        entities.append( [cell.get_text(strip=True) for cell in cells])

    data = [{'Name': entity[0], 'Address': entity[1], 'Type': entity[2], 'Program(s)': entity[3], 'List': entity[4], 'Score': entity[5]} for entity in entities]

    # Close the webdriver
    driver.quit()
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)


