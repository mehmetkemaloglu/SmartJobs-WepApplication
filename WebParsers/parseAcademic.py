import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re

def parseUrl(url,parseAllPages):
    print("parsing ", url)
    #r = requests.get('https://academicpositions.com/find-jobs/PhD~Postdoc-in-all-by-all-in-all/wireless%20sensor%20networks/1')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver=webdriver.Chrome(executable_path="C:/Users/ASUS/Desktop/chromedriver/chromedriver.exe",options=chrome_options);
    driver.get(url)
    #source = BeautifulSoup(r.content,"lxml")
    source = BeautifulSoup(driver.page_source,"lxml")
    results = source.find_all("div", attrs={"class": "ais-hits--item"})
    w = type(results)
    jobs=[]
    for i in results:
        for j in i.contents:
            if type(j)==type(i) and "job" in j.get("class"):
                link=j.find("a",attrs={"class":"job__title js-gtm-joblink"})
                f = link.attrs.get("data-gtm")
                dict = json.loads(f)

                linkstring="https://academicpositions.com"+link.attrs.get("href")
                dict["link"]=linkstring
                datestring = j.find("div", attrs={"class": "hide-lg job__location"}).text.strip()
                dict["dateString"]=datestring
                loc=j.find("div",attrs={"class":"job__location"})
                location=""
                if loc!=None:
                    for k in loc.find_all("a",attrs={"class":"job__location-link"}):
                        location+=k.text+","
                if len(location) >0:
                    location=location[0:-1]
                dict["location"]=location

                driver.get(linkstring)
                newsource=BeautifulSoup(driver.page_source,"lxml")
                tableTag=newsource.find("div",attrs={"class":"job-details-table-wrapper"})
                dict["JobDescription"]=newsource.find("div",attrs={"class":"job-content"}).text.strip()

                for tableRow in tableTag.find_all("tr"):
                    rowName=tableRow.find("td",attrs={"class":"job-details-left-column"}).text.strip()
                    if rowName=="Job Types" or rowName=="Fields":
                        jobtypes=[]
                        types=tableRow.find_all("span",attrs={"class":"field-item"})
                        for jobtype in types:
                            item=jobtype.text.strip()
                            if item.endswith(","):
                                item=item[0:-1]
                            jobtypes.append(item)
                        dict[rowName]=jobtypes

                    else:
                        if rowName == "Published":
                            rowName = "PublishDate"
                        elif rowName == "Application deadline":
                            rowName = "Deadline"
                        dict[rowName]=tableRow.find("td",attrs={"class":"job-details-right-column"}).text.strip()
                jobs.append(dict)
                #print(f)
    file = open("jobs.txt", "a+")
    for i in jobs:
        job=(json.dumps(i))
        file.write(job)
    file.close()
    if(parseAllPages):
       nextLink=source.find("a",attrs={"class":"ais-pagination--link pagination-controls__item","aria-label":"Next"})
       nextpagejobs=[]
       if nextLink:
            nextpagejobs=parseUrl(nextLink.get("href"),True)
       jobs.append(nextpagejobs)
    print("parsing done ", url)
    return json.dumps(jobs)


def formURL(keyword,jobtypes,fields,locations,employers):
    baseUrl="https://academicpositions.com/find-jobs/"
    jobtypesString=listToString(jobtypes)
    fieldsString=listToString(fields)
    locationsString=listToString(locations)
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
parseUrl(formURL("wireless",["Professor","PhD","Postdoc"],["Engineering","Computer Science"],["Europe","France"],["CEA Tech"]),True)
