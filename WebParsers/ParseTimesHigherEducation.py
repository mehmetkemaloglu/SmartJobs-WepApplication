#!/usr/bin/env python
# coding: utf-8

# In[24]:


from bs4 import BeautifulSoup
import requests
import time, os


# In[25]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver


# In[26]:


keywords = "wireless sensor network"
job_search = "https://www.timeshighereducation.com/unijobs/listings/postdocs/?Keywords="
job_query = job_search + keywords.replace(' ', '+') + '&sort=Date#browsing'


# In[27]:


page = requests.get(job_query).text
soup = BeautifulSoup(page, 'html5lib')


# In[28]:


soup.find('ul', id='listing')


# In[29]:


driver = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver.exe")
driver.get(job_query)


# In[30]:


driver.page_source[:1000]


# In[31]:


soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[32]:


soup.find('ul', id='listing')


# In[33]:


listing_ul = soup.find('ul', id='listing')

for li in listing_ul.find_all('h3'):
    print(li.text.strip())


# In[34]:


headings = []
for li in listing_ul.find_all('h3'):
    headings.append(li.text.strip())


# In[35]:


print(headings)


# In[36]:


listing_h3 = soup.find('h3', {"class": "lister__header"})
links = []
for li in listing_ul.find_all('a', href=True):
    links.append(li["href"])


# In[37]:


print(links)


# In[38]:


ids = []
for li in listing_ul.find_all('li'):
    if(li.get('id')) is not None:
        ids.append(li.get('id'))


# In[39]:


idnumbers = []
for i in ids:
    idnumbers.append(i.partition('-')[2])
print(idnumbers)


# In[40]:


reallinks = []
for k in idnumbers:
    reallinks.append("https://www.timeshighereducation.com/unijobs/listing/" + k)
print(reallinks)
print(len(reallinks))


# In[41]:


alldescriptions = []
for link in reallinks:
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html5lib')
    driver = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver.exe")
    driver.get(link)
    driver.page_source[:1000]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listing_ul2 = soup.find('div', {"class":'block fix-text job-description'})
    alldescriptions.append(listing_ul2.text.strip())


# In[43]:


print(alldescriptions)


# In[ ]:




