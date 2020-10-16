import requests
from bs4 import BeautifulSoup

LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    indeed_result = requests.get(INDEED_URL)

    indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

    pagination = indeed_soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    # delete last one[next] from pages
    # pages = pages[0:-1]

    max_page = pages[-1]

    return max_page


def extract_indeed_jobs(last_page):
    #    for page in range(last_page):
    result = requests.get(f"{INDEED_URL}&start={0 * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    jobs = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    # print(jobs)

    for job in jobs:
        job_info = extract_job(job)
        print(job_info)


def extract_job(job_html):
    # TITLE
    title = job_html.find("h2", {"class": "title"}).find("a")["title"]

    # COMPANY
    company = job_html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor != None:
        company = (company_anchor.string).strip()
    else:
        company = (company.string).strip()

    # LOCATION
    location = job_html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    return {"title": title, "company": company, "location": location}
