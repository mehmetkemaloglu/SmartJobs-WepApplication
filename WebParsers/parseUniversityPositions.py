from bs4 import BeautifulSoup
import requests
import time, os


# In[25]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

#keywords = "wireless networks"
baseURL= "https://www.universitypositions.eu/jobs/"
baseURL2 = "?sort=relevance&page="
#url=job_search + keywords.replace(' ', '%20') + '/category/294?sort=relevance&page='
headers=[]
linkList=[]

fieldsToIdMap={
  "computer engineering": "327",
    "anthropology": "324", 
    "linguistics ": "337",
    "architecture and design": "325", 
    "literature": "338", 
    "biology": "326", 
    "mathematics": "339", 
    "chemistry": "334", 
    "medicine": "340", 
    "computer science": "327", 
    "philosophy": "329", 
    "cultural studies": "335", 
    "physics": "330", 
    "earth science": "331", 
    "political science": "344", 
    "economy": "328", 
    "psychology": "341",
    "educational sciences": "347", 
    "social science": "343", 
    "farming science": "336", 
    "space science": "342", 
    "history": "332",
    "technology": "345", 
    "legal ": "333",
    "theology": "346",
    "electrical engineering": "814"
}
jobTypeToIdMap={
    "administrative work": "882", 
    "postdoc": "303",
    "research engineer": "299",
    "associate professor": "292",
    "postgraduate": "297",
    "research manager": "298",
    "bioinformatician": "291",
    "professor": "304",
    "researcher": "296",
    "dean / head of department": "293",
    "programmer": "305",
    "senior lecturer": "307",
    "lecturer / assistant professor": "302",
    "research assistant": "295",
    "senior research associate": "306",
    "phd": "294",
    "research director": "300",
    "staff scientist": "301" 
}

def parseJobListPages(url,pageNum,parseAllPages):
    # category/294 means PHD
    job_query = url+baseURL2+str(pageNum)
    page = requests.get(job_query).text
    soup = BeautifulSoup(page, 'html5lib')
    driver = webdriver.Chrome("C:/Users/Mr. Kemaloglu/PycharmProjects/chromedriver.exe")
    driver.get(job_query)
    driver.page_source[:1000]
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    fullJobListHTML = soup.find('div', {"class": "col-md-12 job-list-header"})

    isLastPage=True
    for header in fullJobListHTML.find_all('h2'):
        headers.append(header.text.strip())


    for links in fullJobListHTML.find_all('a',  {"class": "company-logo"}):
        link=links["href"]
        if link.find("jobs")==-1:
            linkList.append(link)
        else:
            if link.find("page=")!=-1 and int(link[link.find("page=")+5:])>pageNum:
                isLastPage=False

    if isLastPage is not True and parseAllPages:
        parseJobListPages(url,pageNum+1,True)


def urlCreator(keywords,jobtypes,fields,locations,employers):
    urls=[]
    part1s=[]
    part2s=[]
    part3=''
    isCategory=False
    if keywords:
        for keyword in keywords:
            part1="keywords/"+keyword.replace(' ', '%20')
            part1s.append(part1)
    if locations:
        for location in locations:
            part2="location/"+location.replace(' ', '%20')
            part2s.append(part2)
    for jobtype in jobtypes:
        if jobtype.lower() in jobTypeToIdMap:
            part3+=str(jobTypeToIdMap[jobtype.lower()])+","
            isCategory=True
    for field in fields:
        if field.lower() in fieldsToIdMap:
            part3+=str(fieldsToIdMap[field.lower()])+","
            isCategory=True
        if field.lower in jobTypeToIdMap:    
            part3+=str(jobTypeToIdMap[field.lower()])+","
            isCategory=True
    if isCategory:
        part3="category/"+part3
        part3=part3[:-1] 

    if part1s:
        for part1 in part1s: 
            if part2s:   
                for part2 in part2s:
                    url=baseURL+part1+"/"+part2+"/"+part3
                    urls.append(url)
            else:
                url=baseURL+part1+"/"+part3
                urls.append(url)
    else:
        for part2 in part2s:
            url=baseURL+part2+"/"+part3
            urls.append(url)
    return urls

print(urlCreator([], ["Postdoc","PHD"], ["Computer Science", "spacE Science"], ["Sweden","Ukrain"], "a"))


def searchJob(keywords,jobtypes,fields,locations,employers,parseAllPages):
    #headers=[]
    #linkList=[]
    urls=urlCreator(keywords,jobtypes,fields,locations,employers)
    print(urls)
    for url in urls:
        parseJobListPages(url,1,parseAllPages)
    print(linkList)
    print(headers)

    alldescriptions = []
    for link in linkList:
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'html5lib')
        driver = webdriver.Chrome("C:/Users/Mr. Kemaloglu/PycharmProjects/chromedriver.exe")
        driver.get(link)
        driver.page_source[:1000]
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        description=soup.find('div', {"class": "col-lg-12"})
        alldescriptions.append(description)


    #descriptions have <h> <p> so a function is neccessary to get rid of them
    print(alldescriptions)

#searchJob(["wireless networks","edge computing"], [], ["Computer Science"], ["Sweden"], "a",True)

#print(alldescriptions)
