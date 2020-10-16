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
        title = job.find("h2", {"class": "title"}).find("a")["title"]
        print(title)
