import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import os
import datetime
from random import randint
import click

# relevant data for searches

keyword = "test"
location = ['Zürich', '32325', '198']
df_columns = ["Jobs", "URL"]
# pd.set_option('display.max_colwidth', 0)
dir_path = os.path.realpath(os.path.dirname(__file__))
csv_file = os.path.join(dir_path, "jobs_" + keyword + ".csv")
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
csv_file_timestamped = os.path.join(dir_path, "jobs_" + keyword + timestamp + ".csv")
random_search_id = randint(100000000000000000000000000000000, 999999999999999999999999999999999)
# print('random_search_id is ', random_search_id)
data_test_zurich = {'__seo_search':'search',
                    '__search_freetext':keyword,
                    '__search_city':location[0],
                    'seal':random_search_id,
                    '__search_city_location_id':location[1],
                    '__search_city_country':location[2],
                    '__search_city_perimeter':'100',
                    'search_id':random_search_id,
                    'search_simple':'suchen'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept-Language':'en-US,en;q=0.5',
        'Origin':'https://www.freelance.de',
        'Referer':'https://www.freelance.de/Projekte/K/IT-Entwicklung-Projekte/?_offset=',
        'Connection':'keep-alive'
        }
def process_jobs(csv_file, all_jobs, csv_file_timestamped) -> None:
    if os.path.exists(csv_file):
        job_list_df = pd.read_csv(csv_file)
        job_list_df_new = pd.DataFrame(columns = df_columns)
        
        for job in all_jobs.values:
            if job[1] not in job_list_df.values:
                job_list_df_new.loc[len(job_list_df_new)] = job
        print("Length of dataframe: ", print(len(job_list_df_new.index)))
        if not job_list_df_new.empty:
            print("New jobs:")
            print(job_list_df_new.to_markdown(tablefmt="fancy_grid"))
            job_list_df_new.to_csv(csv_file_timestamped)
        else: print("There are no new jobs for this searchterm")
        all_jobs.to_csv(csv_file)
    else:
        print("No previous jobs found for this searchterm, new jobs found: ")
        print(all_jobs)
        all_jobs.to_csv(csv_file)
        
def jobs_info(soup, df, website):
    # get all jobs
    jobs = soup.find_all("div", {"class":"list-item-content"})
    for job in jobs:
        job_details =[text for text in job.stripped_strings]
        a_tags = job.find_all('a', href=True)
        
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
        df.loc[len(df)] = job_details_parsed
    return df

@click.command()
@click.option('--website', default="no_website", help='Insert webpage to parse')
def parse_website(website):
    with requests.Session() as ss:
        all_jobs = pd.DataFrame(columns = df_columns)
        url = '{domain}/Projekte/K/IT-Entwicklung-Projekte/?_offset='.format(domain = website)
        ss.headers = headers
        response1 = ss.post(url, data=data_test_zurich)
        soup1 = BeautifulSoup(response1.text, "html.parser")
        all_jobs = jobs_info(soup1, all_jobs, website)
        
        pagination1 = soup1.find('div', id='pagination').p
        next_pages = math.ceil((int(pagination1.text.split()[3]) - 20) / 20)
        
        # go through the next pages and scrape
        for pages in range(1, next_pages + 1):
            offset = pages * 20
            url_next = '{domain}/Projekte/K/IT-Entwicklung-Projekte/?_offset={offset}&__search_sort_by=1&search_id={id}'.format(domain = website, offset = offset, id = random_search_id)
            response_next = ss.get(url_next)
            soup_next = BeautifulSoup(response_next.text, "html.parser")
            all_jobs = jobs_info(soup_next, all_jobs, website)
            # following is to doublecheck if we are still in the same search results
            # pagination_next = soup_next.find('div', id='pagination').p
            # print(url_next)   
            # print(pagination_next.text.split())
        
        # read csv file and write into it new entries
        process_jobs(csv_file, all_jobs, csv_file_timestamped)
    
if __name__ == '__main__':
    parse_website()
