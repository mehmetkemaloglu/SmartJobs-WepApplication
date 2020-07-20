#!/usr/bin/env python
# coding: utf-8

# In[5]:

from bs4 import BeautifulSoup
from ..constants import chromeDriverPath
from selenium.webdriver.chrome.options import Options
import re
from selenium import webdriver

fakeJobs = ["Haven’t found what you’re looking for?", "A message to our candidates"]
nextPage = ""
allJobs = []
def searchJob(keyword, jobtypes, fields, locations, employers, parseAllPages=True, recent=False):
    global nextPage
    global allJobs
    allJobs = parseUrl(formURL(keyword, jobtypes, fields, locations, employers), parseAllPages, recent).copy()
    while nextPage != "":
        allJobs = allJobs + parseUrl(nextPage, parseAllPages, recent)

    return allJobs

    #return parseUrl(formURL(keyword, jobtypes, fields, locations, employers), parseAllPages, recent)


def parseUrl(url, parseAllPages, recent=False):
    try:
        global nextPage
        print("parsing this: " + url)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chrome_options);
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listing_ul = soup.find('ul', id='listing')
        headings = []
        for li in listing_ul.find_all('h3'):
            if not ("message" in li.text.strip()):
                headings.append(li.text.strip())
        ids = []
        if recent:
            when = listing_ul.find_all('li', {"class": 'job-actions__action pipe'})
            print(len(when))
            for li in listing_ul.find_all('li'):
                if (li.get('id')) is not None:
                    ids.append(li.get('id'))
            ids = ids[:len(ids) - len(when)]
        else:
            print("I am in else")
            next = soup.find('a', {"title": 'Next page'})
            if next is not None:
                nextPage = "https://www.timeshighereducation.com" + next['href']
                print("NextPage: " + nextPage) #Left here
            else:
                nextPage = ""
            for li in listing_ul.find_all('li'):
                if (li.get('id')) is not None:
                    ids.append(li.get('id'))
        idnumbers = []
        for i in ids:
            idnumbers.append(i.partition('-')[2])
        print(idnumbers)
        reallinks = []
        for k in idnumbers:
            if (k != '204135'):
                reallinks.append("https://www.timeshighereducation.com/unijobs/listing/" + k)
        print(reallinks)
        print(len(reallinks))
    
        jobs = []
        alldescriptions = []
        counter = 0
    
        for link in reallinks:
            print("parsing link: " + link)
            dict = {}
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            grid = soup.find('div', {"class": "grid"})
            heading = grid.find_all("div", {"class": "grid-item"})[0].find_all("h1", recursive=False)[0].text.strip()
            print(heading)
            """
            dict["name"] = headings[counter]
            dict["Title"] = headings[counter]
            """
            dict["name"] = heading
            dict["Title"] = heading
            if not heading in fakeJobs:
                listing_ul2 = soup.find('div', {"class": 'block fix-text job-description'})  # for description
                desc = listing_ul2.text.strip()
                des = desc.replace("\n", "")
                de = des.replace("\xa0", "")
                d = de.replace("\u200b", "")
                dict["JobDescription"] = d
                dict["jobhtml"]=str(listing_ul2)
                dict["id"] = idnumbers[counter]
                dict["link"] = reallinks[counter]
    
                recruiter = soup.find('div', {"class": 'cf margin-bottom-5 job-detail-description__recruiter'})
    
                dict["Employer"] = recruiter.find('dd').text.strip()
                dict["category"] = recruiter.find('dd').text.strip()
                location = soup.find('div', {"class": 'cf margin-bottom-5 job-detail-description__location'})
                dict["location"] = location.find('dd').text.strip()
                dict["Job location"] = location.find('dd').text.strip()
                publishdate = soup.find('div', {"class": 'cf margin-bottom-5 job-detail-description__posted-date'})
                dict["PublishDate"] = publishdate.find('dd').text.strip()
                enddate = soup.find('div', {"class": 'cf margin-bottom-5 job-detail-description__end-date'})
                dict["Deadline"] = enddate.find('dd').text.strip()
                dict["website"]="the"
                fields = soup.find('div',
                                   {"class": 'cf margin-bottom-5 job-detail-description__category-AcademicDiscipline'})
                if fields is not None:
                    dict["Fields"] = fields.find('dd').text.strip().replace("\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t", "").split(
                        ", ")
                else:
                    dict["Fields"] = []
                dict["dateString"] = ""
                dict["variant"] = []
                alldescriptions.append(listing_ul2.text.strip())
                counter += 1
                jobs.append(dict)
        return jobs
    except Exception as e:
        print(str(e)+" error in THE parser")
        return []
    

def formURL(keyword, jobtypes, fields, locations, employers):
    keywords = "network"
    job_search = "https://www.timeshighereducation.com/unijobs/listings/"
    job_query = job_search + keywords.replace(' ', '+') + '&sort=Date#browsing'
    fieldsString = ""
    jobtypesString = ""
    if len(fields) > 0:
        if ("comp" in fields[0]) or ("Comp" in fields[0]):
            fieldsString = "computer-science"
        elif ("elect" in fields[0]) or ("Elect" in fields[0]):
            fieldsString = "electrical-and-electronic-engineering"
        else:
            fieldsString = "engineering-and-technology"

    if len(jobtypes) > 0:
        if ("Post" in jobtypes[0]) or ("post" in jobtypes[0]) or ("Phd" in jobtypes[0]) or ("phd" in jobtypes[0]):
            jobtypesString = "postdocs"
        elif ("Rese" in jobtypes[0]) or ("rese" in jobtypes[0]):
            jobtypesString = "research-fellowships"
        elif ("Prof" in jobtypes[0]) or ("prof" in jobtypes[0]):
            jobtypesString = "professors-chairs"
        else:
            jobtypesString = ""
    else:
        jobtypesString = ""

    baseUrl = "https://www.timeshighereducation.com/unijobs/listings/"
    locationsString = ""
    if len(locations) > 0:
        locationsString = adaptFieldString(locations[0].lower())
    keywordString = adaptString(keyword)
    resultUrl = baseUrl + fieldsString + "/" + locationsString + "/" + jobtypesString + "/?keywords=" + keywordString + '&sort=Date#browsing'
    print(resultUrl)
    return resultUrl


def adaptString(word):
    return re.sub("\s+", "+", word.strip())


def adaptFieldString(word):
    return re.sub("\s+", "-", word.strip())
