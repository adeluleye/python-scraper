import requests

base_url = 'http://technologies.unc.edu'
#web_srape_url = 'http://technologies.unc.edu/technologies?limit=288'

# get response
r = requests.get(base_url + '/technologies?limit=288')

# import BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('div', attrs={'class':'technology'})

urls = []
for result in results:
    url = base_url + result.find('a')['href']
    urls.append((url))

# save to a tabular structure
import pandas as pd
df_url = pd.DataFrame(urls, columns=['url'])

# write df to csv
df_url.to_csv('urls.csv', index=False, encoding='utf-8')

#loop through each of the url
records = []
for url in urls:
    pub_request = requests.get(url)
    pub_soup = BeautifulSoup(pub_request.text, 'html.parser')
    pub_results = pub_soup.find_all('div', attrs={'class':'technology'})
    
    records.append((pub_results))

data = []
for record in records:
    
    pub_title = record[0].find('h1').text
    pub_description = ''.join(record[1].find('div', class_='content').text[0:-1].split('\xa0')[0:-1])
    related_pub_title = record[1].find('div', class_='content').find_next('a').contents[0]
    related_pub_link = record[1].find('div', class_='content').find_next('a')['href']
    research_inventor = record[1].find('dd', class_='inventor').find('a').text
    research_inventor_link = base_url + record[1].find('dd', class_='inventor').find('a')['href']
    managed_by = record[1].find('dd', class_='manager').text
    managed_by_link = base_url + record[1].find('dd', class_='manager').find('a')['href']
    patent_protection = record[1].find('div', class_='information').find_next('dl').contents[-1].text
    (techy, technology_number) = record[0].find('em').text.split(' ')
    data.append((pub_title, 
                 pub_description, 
                 related_pub_title, 
                 related_pub_link, 
                 research_inventor,
                research_inventor_link,
                managed_by,
                managed_by_link,
                patent_protection,
                technology_number))

df = pd.DataFrame(data, columns=['pub_title', 
                                 'pub_description', 
                                 'related_pub_title', 
                                 'related_pub_link',
                                'research_inventor',
                                'research_inventor_link',
                                'managed_by',
                                'managed_by_link',
                                'patent_protection',
                                'technology_number'])

df.to_csv('publication_scrape.csv', index=False, encoding='utf-8')