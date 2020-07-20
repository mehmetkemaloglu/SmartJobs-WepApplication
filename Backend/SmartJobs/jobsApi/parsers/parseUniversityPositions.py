from bs4 import BeautifulSoup
from ..constants import chromeDriverPath
from selenium.webdriver.chrome.options import Options
import re

from selenium import webdriver
from datetime import date, timedelta


def search(keyword,jobtypes,fields,locations,employers,parseAllPages=True, recent=False):

        headers = []
        urlfunc=formURL(keyword, jobtypes, fields, locations, employers)
        job_query =urlfunc [0]
        variantList=urlfunc[1]
        print("parsing this : "+job_query)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chrome_options);
        linkList=[]
        soup=""

        publish_dates = []

        def parseJobListPages(pageNum):
            #job_query = formURL(keyword, jobtypes, fields, locations, employers)
            nonlocal soup
            nonlocal job_query
            nonlocal publish_dates

            newquery = job_query + "&page=" + str(pageNum)
            print("parsing: "+newquery)
            driver.get(newquery)
            driver.page_source[:1000]
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            fullJobListHTML = soup.find('div', {"class": "col-md-12 job-list-header"})



            if recent:

                linkarray = []
                jobrows=soup.find_all("div",{"class":"col-sm-12 media job-listing normal-job"})

                dates=[]
                links=[]
                for jobrow in jobrows:
                    headers.append(jobrow.find('h2', {"class": "media-heading"}).text.strip())
                    dates.append(jobrow.find('span', {"class": "job-date"}))
                    links.append(jobrow.find('a', {"class": "company-logo"}))
                for link in links:
                    linkarray.append(link["href"])
                #dates = links.find_all('span', {"class": "job-date"})
                today=date.today()
                yesterday = today - timedelta(days=1)
                date_time1 = yesterday.strftime("%Y-%m-%d")
                date_time2= today.strftime("%Y-%m-%d")
                ccounter = 0


                for jjobdate in dates:
                    jjobdate = jjobdate.text.strip()
                    jjobdate = (jjobdate.partition(' ')[2])

                    if jjobdate == date_time1 or jjobdate==date_time2:
                        publish_dates.append(jjobdate)
                        linkList.append(linkarray[ccounter])
                    else:
                        return False #stop when an older job is found
                    ccounter += 1
            else:

                for header in fullJobListHTML.find_all('h2'):
                    headers.append(header.text.strip())

                datess = soup.find_all('span', {"class": "job-date"})
                for jjobdates in datess:
                    jjobdatess = jjobdates.text.strip()
                    jjobdatesss = (jjobdatess.partition(' ')[2])
                    publish_dates.append(jjobdatesss)

                for links in fullJobListHTML.find_all('a', {"class": "company-logo"}):
                    link = links["href"]
                    if link.find("jobs") == -1:
                        linkList.append(link)
                    #else:
                        #if link.find("page=") != -1 and int(link[link.find("page=") + 5:]) > pageNum:
                         #   isLastPage = False

            return True



            #if isLastPage == False:
             #   parseJobListPages(pageNum+1)
        recentnotfound=parseJobListPages(1)
        if (recent and recentnotfound) or not recent:
            pagination = soup.find('ul', {"class": "pagination"})
            if pagination is not None:
                lus = pagination.find_all('li')
                if len(lus)>0:
                    a=lus[-1].find_all('a',attrs={"class":None})
                    if len(a)>0:
                        if a[0].text=="»":
                            lastpagenum=int(a[0]["href"].split("=")[-1])
                            for i in range(2,lastpagenum+1):
                                rnf=parseJobListPages(i)
                                if not rnf:
                                    break

        jobs = []
        alldescriptions = []
        counter = 0
        print(str(len(linkList))+" jobs found in UP")
        for link in linkList:
            dict = {}
            print("parsing job: "+link)
            driver.get(link)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            dict["link"] = link

            dict["id"] = link[-5:]

            dict["dateString"] = ""
            dict["Title"] = headers[counter]
            dict["name"] = headers[counter]
            dict["website"] = "up"
            dict["PublishDate"] = publish_dates[counter]
            if len(variantList) > 0:
                dict["Job Types"] = variantList[0]
            dict["variant"] = variantList

            description = soup.find('div', {"class": "col-lg-12"})
            dict["jobhtml"]=str(soup.find("div",attrs={"class":"inner-box","id":("job-"+dict["id"])}))
            desc = description.text.strip()
            des = desc.replace("\n", "")
            de = des.replace("<h1>", "")
            d = de.replace("</p>", "")
            if "JOB DESCRIPTION" in d:
                try:
                    dict["JobDescription"] = d.split(headers[counter] + "JOB DESCRIPTION")[1]
                except:
                    dict["JobDescription"] = d.split("JOB DESCRIPTION")[1]
                alldescriptions.append(description)
            elif headers[counter] in d:
                dict["JobDescription"] = d.split(headers[counter])[1]
                alldescriptions.append(description)
            else:
                dict["JobDescription"] = d
                alldescriptions.append(description)

            side = soup.find('div', {"class": "visible-sm visible-xs"})
            realdeadline = "Unspecified"
            for deadline in side.findAll('p'):
                if "2020" in deadline.text.strip():
                    realdeadline = deadline.text.strip()
                    dict["Deadline"] = realdeadline
                else:
                    dict["Deadline"] = realdeadline

            titles = []
            for title in side.findAll('h3'):
                puretitle = title.text.strip()
                titles.append(puretitle)
                if puretitle == "Company":
                    dict["Employer"] = side.find('a').text.strip()
                    dict["category"] = side.find('a').text.strip()
                elif puretitle == "Deadline for application":
                    dict["Deadline"] = realdeadline

            locations = []
            locationslist = side.find('div', {"class": "location-list"})
            if locationslist is not None:
                for li in locationslist.findAll('a'):
                    locations.append(li.text.strip())
                    dict["Job location"] = locations[0]
                    dict["location"] = locations[0]
            else:
                dict["Job location"] = "Unknown"
                dict["location"] = "Unknown"

            categorieslist = soup.find('div', {"class": "cat-list"})
            categories = []
            if categorieslist is not None:
                for li in categorieslist.find_all('a'):
                    categories.append(li.text.strip())

            dict["Fields"] = categories
            counter += 1
            jobs.append(dict)

        return jobs


def formURL(keyword, jobtypes, fields, locations, employers):
    variantList=[]
    fieldsString = ""
    if len(jobtypes) > 0:
        if ("Post" in jobtypes[0]) or ("post" in jobtypes[0]):
            jobtypesString = "category/" + "303"
            variantList.append("Postdoc")
        elif ("Phd" in jobtypes[0]) or ("phd" in jobtypes[0]) or ("PhD" in jobtypes[0]):
            jobtypesString = "category/" + "294"
            variantList.append("Phd")
        elif ("Rese" in jobtypes[0]) or ("rese" in jobtypes[0]):
            jobtypesString = "category/" + "296"
            variantList.append("Researcher")
        elif ("Prof" in jobtypes[0]) or ("prof" in jobtypes[0]):
            jobtypesString = "category/" + "304"
            variantList.append("Professor")
        elif ("lecture" in jobtypes[0]) or ("Lecture" in jobtypes[0]) or ("Assist" in jobtypes[0]) or ("assist" in jobtypes[0]):
            jobtypesString = "category/" + "302"
            variantList.append("Lecturer")
        else:
            jobtypesString = ""
    else:
        jobtypesString = ""

    if len(fields) > 0:
        if jobtypesString != "":
            if ("Comp" in fields[0]) or ("comp" in fields[0]):
                fieldsString = ",327"
            elif ("elect" in fields[0]) or ("Elect" in fields[0]):
                fieldsString = ",814"
        else:
            if ("Comp" in fields[0]) or ("comp" in fields[0]):
                fieldsString = "category/" + "327"
            elif ("elect" in fields[0]) or ("Elect" in fields[0]):
                fieldsString = "category/" + "814"

    locationsString = ""
    baseUrl = "https://www.universitypositions.eu/jobs/"
    if len(locations) > 0:
        locationsString = "location/" + locations[0].lower() + "/"

    if keyword != "":
        keywordString = "keywords/" + adaptString(keyword) + "/"
    else:
        keywordString = ""

    resultUrl = baseUrl + keywordString + locationsString + jobtypesString + fieldsString + "?sort=date"

    return (resultUrl,variantList)

def adaptString(word):
    return re.sub("\s+", "%20", word.strip())
