import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint

# relevant data for searches
random_search_id = randint(100000000000000000000000000000000, 999999999999999999999999999999999)
print('random_search_id is ', random_search_id)
data_test_zurich = {'__seo_search':'search',
                    '__search_freetext':'test',
                    '__search_city':'Zürich',
                    'seal':random_search_id,
                    '__search_city_location_id':'32325',
                    '__search_city_country':'198',
                    '__search_city_perimeter':'100',
                    'search_id':random_search_id,
                    'search_simple':'suchen'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
           'Accept-Language':'en-US,en;q=0.5'}

def jobs_info(html_response):
    soup_job = BeautifulSoup(html_response, "html.parser")
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
    job_details_parsed = [name, link_stripped]
    return job_details_parsed


with requests.Session() as ss:
    url1 = 'https://www.freelance.de/Projekte/K/IT-Entwicklung-Projekte/?_offset='
    url2 = 'https://www.freelance.de/Projekte/K/IT-Entwicklung-Projekte/?_offset=20&__search_sort_by=1&search_id={id}'.format(id = random_search_id)
    url3 = 'https://www.freelance.de/Projekte/K/IT-Entwicklung-Projekte/?_offset=40&__search_sort_by=1&search_id={id}'.format(id = random_search_id)

    response1 = ss.post(url1, data=data_test_zurich, headers=headers)
    response2 = ss.get(url2)
    response3 = ss.get(url3)

    soup1 = BeautifulSoup(response1.text, "html.parser")
    soup2 = BeautifulSoup(response2.text, "html.parser")
    soup3 = BeautifulSoup(response3.text, "html.parser")

    pagination1 = soup1.find('div', id='pagination').p
    pagination2 = soup2.find('div', id='pagination').p
    pagination3 = soup3.find('div', id='pagination').p

    print('Pagination 1 - ', pagination1.text)
    print('Cookies 1 - ', response1.cookies.values())
    print('Pagination 2 - ', pagination2.text)
    print('Cookies 2 - ', response2.cookies.values())
    print('Pagination 3 - ', pagination3.text)
    print('Cookies 3 - ', response3.cookies.values())


       

# soup = BeautifulSoup(response2html, "html.parser")

# jobs = soup.find_all("div", class_="list-item-main")
# job_details = [text for text in jobs[0].stripped_strings]
