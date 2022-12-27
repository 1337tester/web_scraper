import mechanicalsoup
import sys

separator = 40*"*"

def main(args):
    if not args:
        args = ["-"]
    for arg in args:
        if arg != "-":
            print(arg)

def list_jobs(browser):
    for job in browser.page.find_all("div", class_="panel-body single-profile clearfix"):
        job_details = [text for text in job.stripped_strings]
        
        # deleting premium content
        del job_details[1]
        del job_details[1]
        
        # print the list 
        # print(';'.join(job_details))
        print(*job_details, sep = "\n")
        print(separator)
        
    pages = browser.page.select('[id=pagination]')[0].p.text.split(' ')
    print(pages[2], pages[3], pages[4])


browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
)
browser.open("https://www.freelance.de/Projekte/K/IT-Entwicklung-Projekte/")

browser.select_form('[id=__search]')
browser["__search_freetext"] = "test"
# browser["__search_city"] = "Zürich, Bern, Zug"
browser["__search_city"] = "Zürich, Zug"
# browser["__search_city_location_id"] = "32325"
# browser["__search_city_country"] = "198"
# browser["__search_city_country_extended"] = "198"
# browser["__search_city_perimeter"] = "100"
browser["seal"] = "1"
browser["search_id"] = "2344754"


response = browser.submit_selected()
print(response)
print(separator)

list_jobs(browser)

l = browser.links(link_text='Next')
# print(type(l), l)
print(browser.follow_link(l))
print('URL => ', browser.get_url())

list_jobs(browser)

pagess = browser.page.select('[id=pagination]')[0].p.text.split(' ')
print(pagess[2], pagess[3], pagess[4])

if __name__ == "__main__":
    main(sys.argv[1:])