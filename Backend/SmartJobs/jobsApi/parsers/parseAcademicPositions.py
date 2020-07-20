import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re
import time
from .helpers import getContinent
from ..constants import chromeDriverPath


def getHTMLOfJobsInDatabase():
    from ..models import Jobs
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chrome_options);
    jobs=Jobs.objects.filter(jobhtml=None).only("link")
    for job in jobs:
        if job.jobhtml == None:
                print(job.jid)
                driver.get(job.link)
                try:
                    soup=BeautifulSoup(driver.page_source,"lxml")
                    if job.website=="ap":
                        job.jobhtml=str(removeImagesAndCRButton(soup.find("div", attrs={"class": "job-content"})))
                    elif job.website=="the":
                        job.jobhtml=str(soup.find('div', {"class": 'block fix-text job-description'}))
                    else:
                        id=job.link[-5:]
                        job.jobhtml=str(soup.find("div",attrs={"class":"inner-box","id":("job-"+id)}))
                    job.save()
                except Exception as e:
                    print(e.__str__())


def removeImagesAndCRButton(jobContent):
    cnt=jobContent.find("span",attrs={"class":"continue-reading-btn"})
    if cnt:
        cnt.decompose()
    imgs=jobContent.find_all("img")
    for img in imgs:
        img.decompose()
    return jobContent



def searchJob(keyword,jobtypes,fields,locations,employers,parseAllPages=True,recent=False):
    jobs=[]
    if len(locations)>0:
        for location in locations:
            if len(fields) > 0:
                for field in fields:
                    jobs.extend(parseUrl(formURL(keyword, jobtypes, field, location, employers), parseAllPages,recent=recent))
            else:
                jobs.extend(parseUrl(formURL(keyword, jobtypes, "", location, employers), parseAllPages,recent=recent))

    else:
        if len(fields)>0:
            for field in fields:
                    jobs.extend(parseUrl(formURL(keyword, jobtypes, field, "", employers), parseAllPages,recent=recent))
        else:
            jobs.extend(parseUrl(formURL(keyword, jobtypes, "", "", employers), parseAllPages,recent=recent))

    uniqjobs=[]
    #print([job["Title"] for job in jobs])
    for job in jobs:
        check=False
        for uniqjob in uniqjobs:
            if uniqjob["id"]==job["id"]:
                print("same job id: "+uniqjob["id"])
                print(uniqjob["Title"]+" "+job["Title"])
                check=True
                break
        if not check:
            uniqjobs.append(job)

    return uniqjobs


def parsePageSource(driver,items,recent=False):
    jobs = []
    for results in items:
        w = type(results)


        for i in results:
            check=True
            for j in i.contents:
                if type(j) == type(i) and "job" in j.get("class"):
                    link = j.find("a", attrs={"class": "job__title js-gtm-joblink"})
                    f = link.attrs.get("data-gtm")
                    dict = json.loads(f)

                    linkstring = "https://academicpositions.com" + link.attrs.get("href")
                    dict["link"] = linkstring
                    datestring = j.find("div", attrs={"class": "hide-lg job__location"}).text.strip()
                    dict["dateString"] = datestring

                    if recent:
                        """
                        today = datetime.today()
                        yesterday = datetime.today() - timedelta(days=1)
                        yesterdayStr=(calendar.month_name[yesterday.month] + " " + str(yesterday.day) + ", " + str(
                            yesterday.year))
                        todayStr=calendar.month_name[today.month] + " " + str(today.day) + ", " + str(today.year)
                        if datestring==todayStr or datestring==yesterdayStr:
                            check=False
                            break
                        """
                        publish = datestring.split("Closing")[0]
                        if ("days" in publish) or ("month" in publish) or ("year" in publish):
                            print("easdasdasd")
                            check = False
                            break



                    loc = j.find("div", attrs={"class": "job__location"})
                    location = ""
                    if loc != None:
                        for k in loc.find_all("a", attrs={"class": "job__location-link"}):
                            location += k.text + ","
                    if len(location) > 0:
                        location = location[0:-1]
                    dict["location"] = location

                    driver.get(linkstring)
                    print(linkstring+" "+"this")
                    newsource = BeautifulSoup(driver.page_source, "lxml")
                    tableTag = newsource.find("div", attrs={"class": "job-details-table-wrapper"})
                    jobDesc=newsource.find("div", attrs={"class": "job-content"})
                    dict["JobDescription"] = jobDesc.text.strip()
                    dict["jobhtml"]=str(removeImagesAndCRButton(jobDesc))
                    for tableRow in tableTag.find_all("tr"):
                        rowName = tableRow.find("td", attrs={"class": "job-details-left-column"}).text.strip()
                        if rowName == "Job Types" or rowName == "Fields":
                            jobtypes = []
                            types = tableRow.find_all("span", attrs={"class": "field-item"})
                            for jobtype in types:
                                item = jobtype.text.strip()
                                if item.endswith(","):
                                    item = item[0:-1]
                                jobtypes.append(item)
                            dict[rowName] = jobtypes

                        else:
                            if rowName == "Published":
                                rowName = "PublishDate"
                            elif rowName == "Application deadline":
                                rowName = "Deadline"
                            dict[rowName] = tableRow.find("td", attrs={"class": "job-details-right-column"}).text.strip()
                    dict["website"] = "ap"
                    #DBhelper.saveJob(dict)
                    jobs.append(dict)
            if not check:
                break
    return jobs
                # print(f)

def getItems(driver,url,parseAllPages,recent=False):
    try:
        print("parsing this ", url)
        #r = requests.get('https://academicpositions.com/find-jobs/PhD~Postdoc-in-all-by-all-in-all/wireless%20sensor%20networks/1')

        driver.get(url)
        #source = BeautifulSoup(r.content,"lxml")
        if recent:
            #print(driver.find_element(By.xpath("//a[contains(.,'Recent')]")))
            driver.find_element_by_link_text("Recent").click()
            time.sleep(2)
            print("Recent Selected")
        source = BeautifulSoup(driver.page_source, "lxml")

        allresults = []
        items=source.find_all("div", attrs={"class": "ais-hits--item"})
        allresults.append(items)


                    #print(f)
        """
        file = open("jobs.txt", "a+")
        for i in jobs:
            job=(json.dumps(i))
            file.write(job)
        file.close()
        """

        if(parseAllPages):
            if recent:
                nextLink = source.find("a", attrs={"class": "ais-pagination--link pagination-controls__item",
                                                   "aria-label": "Next"})
                check=True
                while nextLink and check:
                    if len(items)>0:
                            i=items[-1]
                            for j in i.contents:
                                if type(j) == type(i) and "job" in j.get("class"):
                                    datestring = j.find("div", attrs={"class": "hide-lg job__location"}).text.strip()
                                    publish=datestring.split("Closing")[0]
                                    if ("days" in publish) or ("month" in publish) or ("year" in publish):

                                        check=False
                                        break
                    if check:
                        driver.find_element_by_link_text("Next").click()
                        time.sleep(1.7)
                        source = BeautifulSoup(driver.page_source, "lxml")
                        items=source.find_all("div", attrs={"class": "ais-hits--item"})
                        allresults.append(items)


                    nextLink = source.find("a", attrs={"class": "ais-pagination--link pagination-controls__item",
                                                       "aria-label": "Next"})


            else:
                nextLink=source.find("a",attrs={"class":"ais-pagination--link pagination-controls__item","aria-label":"Next"})
                nextpagejobs=[]
                while nextLink:
                    driver.find_element_by_link_text("Next").click()
                    time.sleep(1.7)
                    source = BeautifulSoup(driver.page_source, "lxml")
                    items = source.find_all("div", attrs={"class": "ais-hits--item"})
                    allresults.append(items)
                    nextLink = source.find("a", attrs={"class": "ais-pagination--link pagination-controls__item",
                                                       "aria-label": "Next"})
                """
                if nextLink:
                        print("this is "+nextLink.get("href"))
                        nextpagejobs=getItems(nextLink.get("href"),True,recent=False)
                """
                allresults.extend(nextpagejobs)

        """
            try:

                elem = driver.find_element_by_xpath("//a[contains(text(), 'Next')]")
                while True:
                    print(elem.get_attribute("href"))
                    elem.click()
                    time.sleep(1)
                    jobs.extend(parsePageSource(driver))
                    elem = driver.find_element_by_xpath("//a[contains(text(), 'Next')]")
            except Exception as e:
                print(e.__str__())
        """



        return allresults

    except Exception as e:
        print(e)
        print("Error occurred while parsing given url: "+url)
        return []


def parseUrl(url,parseAllPages,recent=False):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chrome_options);
        items=getItems(driver,url,parseAllPages,recent)
        print(len(items).__str__())

        jobs=parsePageSource(driver,items,recent)
        print(str(len(jobs)))
        return jobs
    except Exception as e:
        print(e)
        print("Error occurred while parsing given url: "+url)
        return []


def formURL(keyword,jobtypes,fields,location,employers):

    if keyword=="":
        keyword="all"



    baseUrl="https://academicpositions.com/find-jobs/"

    if len(jobtypes)>0:
        jobtypesString=listToString(jobtypes)
    else:
        jobtypesString="all"

    if fields != "":
        fieldsString=adaptString(fields)
    else:
        fieldsString="all"

    if location != "":
        locationlist=[getContinent(location),location]
        locationsString=listToString(locationlist)
    else:
        locationsString="all"
    employersString=listToString(employers)
    keywordString=adaptString(keyword)
    return baseUrl+jobtypesString+"-in-"+fieldsString+"-by-"+employersString+"-in-"+locationsString+"/"+keywordString+"/1"
def adaptString(word):
    return re.sub("\s+","%20",word.strip())

def listToString(list):

    jobtypesString = ""
    if len(list)>0:
        for jobtype in list:
            jobtypesString+=adaptString(jobtype)+"~"
        jobtypesString=jobtypesString[0:-1]
    else:
        jobtypesString="all"

    return  jobtypesString
#parseUrl('https://academicpositions.com/find-jobs/Professor-in-all-by-all-in-all/wireless/1',True)
#parseUrl(formURL("wireless",["Professor","PhD","Postdoc"],["Engineering","Computer Science"],["Europe","France"],["CEA Tech"]),True)


