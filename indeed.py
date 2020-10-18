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
    jobs_list = []
    for page in range(last_page):
        print(f"# WEB SCRAPING INDEED PAGE : {page}")
        page_url = f"{INDEED_URL}&start={page * LIMIT}"
        result = requests.get(page_url)
        soup = BeautifulSoup(result.text, "html.parser")
        jobs = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        # print(jobs)

        for job in jobs:
            job_info = extract_job(page_url, job)
            # print(job_info)
            jobs_list.append(job_info)

    return jobs_list


def extract_job(page_url, job_html):
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

    # JOB_ID (detail page)
    job_id = job_html["data-jk"]
    detail_page = f"https://www.indeed.com/viewjob?jk={job_id}"

    return {"title": title, "company": company, "location": location, "link": detail_page}


def get_jobs():
    last_indeed_page = extract_indeed_pages()
    indeed_jobs = extract_indeed_jobs(last_indeed_page)
    return indeed_jobs
