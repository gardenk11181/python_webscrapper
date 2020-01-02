import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")  # page의 모든 html을 가져온다.

    pagination = soup.find("div", {"class": "pagination"})  # page number가 있는 block 가져옴

    links = pagination.find_all("a")  # "a"를 리스트로 가져옴
    pages = []
    for link in links[0:-1]:  # 마지막인 next제외하고 for loop 진행
        pages.append(int(link.find("span").string))  # 리스트에서 span 속 텍스트만 가져와서 리스트로 만듬

    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]  # 원하는 요소 출력하기
    company = html.find("span", {"class": "company"})
    if company is None:
        company = "Unknown"
    else:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company.find("a").string)
        else:
            company = str(company.string)
        company = company.strip()  # 양쪽 끝의 빈칸을 없애줌.


    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'title':title,
            'company':company,
            'location':location,
            'link':f"https://www.indeed.com/viewjob?jk={job_id}"
            }

def extract_indeed_jobs(last_page):
    jobs=[]
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for res in results:
            job = extract_job(res)
            jobs.append(job)
    return jobs