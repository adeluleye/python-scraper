import requests

url = 'https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html'

# get response
r = requests.get(url)

# import BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('span', attrs={'class':'short-desc'})

records = []
for result in results:
    date = result.find('strong').text[0:-1] + ', 2017'
    lie = result.contents[1][1:-2]
    explanation = result.find('a').text[1:-1]
    try:
        url = result.find('a')['href']
    #except expression as identifier:
    except ValueError:
        url = None
    
    records.append((date, lie, explanation, url))

# save to a tabular structure
import pandas as pd
df = pd.DataFrame(records, columns=['date', 'lie', 'explanation', 'url'])

# convert date column to pandas datetime
df['date'] = pd.to_datetime(df['date'])

# write df to csv
df.to_csv('trump_lies2.csv', index=False, encoding='utf-8')