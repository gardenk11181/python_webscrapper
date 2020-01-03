import requests
from bs4 import BeautifulSoup

PAGE = 1
URL = "https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    links = soup.find("div",{"class":"s-pagination"}).find_all ("a")
    pages = []
    for link in links:
        page = link.find("span").string
        pages.append(page)
    max_page = pages[-2]
    return int(max_page)


def extract_job(html,link):
    title = html.find("h2").string
    h3 = html.find("h3").find_all("span")
    company = h3[0].string
    if company is None:
        company = "None"
    else:
        company = company.strip()
    location = h3[1].string.strip()
    link = link.button["data-id"]
    return {'title': title,
            'company': company,
            'location': location,
            'link': f"https://stackoverflow.com/jobs/{link}/"
        }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping so page {page+1}")
        count = 0
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        lists = soup.find("div", {"class": "listResults"}).find_all("div",{"class":"grid--cell fl1 mr12"})
        links = soup.find("div", {"class": "listResults"}).find_all("div",{"class":"grid--cell grid fd-column"})
        for list in lists:
            job = extract_job(list,links[count])
            jobs.append(job)
            count = count+1
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs


