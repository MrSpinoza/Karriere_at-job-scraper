# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:42:48 2022

@author: MACEDOLJANB
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Trazilica
search_keyword = ['data-science', 'python']


final_list_job_title=[]
final_list_job_company = []
final_list_job_posted = []
final_list_job_location =[]
final_list_ad_link = []
final_keyword_list = []

for keyword in search_keyword:
    # Trazi koncni broj stranica pretrage
    web_content = requests.get("https://www.karriere.at/jobs/{}".format(keyword)).text
    soup = BeautifulSoup(web_content, "lxml")
    total_page_info = soup.find("span", attrs= {'class': "m-pagination__meta"}).text
    total_page_number = [int(i) for i in total_page_info.split() if i.isdigit()][1]
    
    
    
    def scrap(pg):
        web_content = requests.get("https://www.karriere.at/jobs/{}?page={}".format(keyword,pg)).text
        soup = BeautifulSoup(web_content, "lxml")
        
        # Prazne liste
        job_title_list = []
        company_name_list = []
        job_posted_list = []
        job_location_list = []
        ad_link_list = []
        keyword_list = []
        
        active_jobs = soup.find_all("li", attrs= {'class': "m-jobsList__item"})
        for jobs in active_jobs:
            job_title = jobs.find("h2", attrs = {'class': 'm-jobsListItem__title'})
            company_name = jobs.find("div", attrs = {'class': 'm-jobsListItem__company'})
            job_posted = jobs.find("span", attrs = {'class': 'm-jobsListItem__date'})
            job_location = jobs.find("li", attrs = {'class': 'm-jobsListItem__location'})
            ad_link = jobs.find("a", attrs = {'class': 'm-jobsListItem__titleLink'})
            if job_title != None:
                job_title_list.append(job_title.text)
                company_name_list.append(company_name.text)
                job_posted_list.append(job_posted.text.strip().split()[1])
                job_location_list.append(job_location.text.split()[0].replace("Wien","Vienna").replace(",",""))
                ad_link_list.append(ad_link['href'])
                keyword_list.append(keyword)
        return [job_title_list,company_name_list,job_posted_list, job_location_list, ad_link_list, keyword_list]
           
    
    
    for i in range(1,total_page_number):
        final_list_job_title.append(scrap(i)[0])
        final_list_job_company.append(scrap(i)[1])
        final_list_job_posted.append(scrap(i)[2])
        final_list_job_location.append(scrap(i)[3])
        final_list_ad_link.append(scrap(i)[4])
        final_keyword_list.append(scrap(i)[5])

# pretvara listu lista u jednu listu
flat_list_title = [item for sublist in final_list_job_title for item in sublist]
flat_list_company = [item for sublist in final_list_job_company for item in sublist]
final_list_job_posted = [item for sublist in final_list_job_posted for item in sublist]
final_list_job_location = [item for sublist in final_list_job_location for item in sublist]
final_list_ad_link = [item for sublist in final_list_ad_link for item in sublist]
final_keyword_list = [item for sublist in final_keyword_list for item in sublist]

# pravi df od lista
df = pd.DataFrame({
    'serch_keyword': final_keyword_list,
    'job_title':flat_list_title, 
    'company_name':flat_list_company, 
    'job_posted_date': final_list_job_posted,
    'job_location':final_list_job_location,
    'job_link': final_list_ad_link
    })

# Cuvanje podataka u csv format
dt_name="Job_Search_Results_For"
for index in search_keyword:
    dt_name = dt_name+"_"+index
df.to_csv(dt_name+".csv")

print("Saved {}.csv!".format(dt_name))