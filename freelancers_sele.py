from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import sys
import os
import datetime

separator = 40*"*"
keyword = "test"
city = "Zürich"
website = "https://www.freelance.de"
search_link = "/Projekte/K/IT-Entwicklung-Projekte/"
all_jobs = []
dir_path = os.path.realpath(os.path.dirname(__file__))
csv_file = os.path.join(dir_path, "jobs_" + keyword + ".csv")
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
csv_file_timestamped = os.path.join(dir_path, "jobs_" + keyword + timestamp + ".csv")

def jobs_info(soup_job):
    job_details = [text for text in soup_job.stripped_strings]
    a_tags = soup_job.find_all('a', href=True)    
        
    # assigning strings to a meaningfull parameter
    name = job_details[0]
    to_strip = "/highlight=" + keyword
    link = website + a_tags[0]['href']
    link_stripped = link.rstrip(to_strip)
    techstack = job_details[3:-6]
    start = job_details[-6]
    location = job_details[-5]
    office_type = job_details[-4]
    added = job_details[-3]
    
    # print(name, *techstack, start, location, office_type, added, sep = "\n")
    job_details_final = [name, link_stripped]
    return job_details_final
    
def check_pagination(pagination):
    pages = pagination.text.split(' ')
    print(pages[1], pages[2], pages[3])

# selectors
freetext_css = '#__search_freetext'
city_css = '#__search_city'
# city_autocompleter_css = '#project_city_autocompletion'
city_selectfirst_css = '.place-autocompleter > a:nth-child(1)'
city_distance_css = 'div.col-sm-2:nth-child(3) > div:nth-child(2) > button:nth-child(1)'
city_distance_100km_css = 'div.col-sm-2:nth-child(3) > div:nth-child(2) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(5) > a:nth-child(1)'
search_css = '#search_simple'
job_info_css = '.project-list > div'
pagination_css = '[id=pagination] > p'
next_css = '[aria-label=Next]'

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
# to supress the error messages/logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
pd.set_option('display.max_colwidth', None)

try:
    chrome_driver.get(website + search_link)
    
    # insert search keyword            
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, freetext_css)))
    input_freetext = chrome_driver.find_element(By.CSS_SELECTOR, freetext_css)
    input_freetext.send_keys(keyword)
    
    input_city = chrome_driver.find_element(By.CSS_SELECTOR, city_css)
    input_city.click()
    sleep(1)
    input_city.send_keys(city)
    
    # select first choice
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, city_selectfirst_css)))
    city_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, city_selectfirst_css)
    city_dropdown.click()
    
    # select radius from city
    chrome_driver.find_element(By.CSS_SELECTOR, city_distance_css).click()
    chrome_driver.find_element(By.CSS_SELECTOR, city_distance_100km_css).click() 
    
    # submit search
    chrome_driver.find_element(By.CSS_SELECTOR, search_css).click()    
    
    # scraping the first page of jobs
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, job_info_css)))
    jobs_elem = chrome_driver.find_elements(By.CSS_SELECTOR, job_info_css)
    for job in jobs_elem:
        soup_job = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
        # TODO change .append to .concat
        all_jobs.append(jobs_info(soup_job))
    
    # steering through the other pages
    next = chrome_driver.find_element(By.CSS_SELECTOR, next_css)
    while next:
        next.click()
        WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, job_info_css)))
        jobs_elem = chrome_driver.find_elements(By.CSS_SELECTOR, job_info_css)
        for job in jobs_elem:
            soup_job = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
            all_jobs.append(jobs_info(soup_job))
        try:
            next = chrome_driver.find_element(By.CSS_SELECTOR, next_css)
        except NoSuchElementException:
            next = None
    
    # read csv file and write into it new entries
    job_list_df = pd.read_csv(csv_file)
    job_list_df_new = pd.DataFrame()
    for job in all_jobs:
        if job[1] not in job_list_df.values :
            # print(*job, sep = "\n")
            # print(separator)
            series = pd.Series(job)
            job_list_df_new = job_list_df_new.append(series, ignore_index=True)
    job_list_df = pd.DataFrame(all_jobs)
    # print(csv_file)
    if not job_list_df_new.empty:
        print("New jobs:", job_list_df_new)
        job_list_df_new.to_csv(csv_file_timestamped)
    else: print("There are no new jobs for this searchterm")
    job_list_df.to_csv(csv_file)
    
except NoSuchElementException as ex:
    print(ex.args)
    
finally:
    chrome_driver.close()
