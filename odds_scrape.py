import requests
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.betexplorer.com/basketball/usa/nba/fixtures/"



# Specify the path to chromedriver
driver_path = '/Users/jamiewelsh/chromedriver_mac64'  # Replace with the actual path to chromedriver

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Open the webpage using Selenium
driver.get(URL)

# Wait for a few seconds to ensure that dynamic content is loaded
time.sleep(5)  # You may need to adjust this depending on the page load time

# Get the updated HTML content
html = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table containing the matches
table_matches = soup.find('table', attrs={'class': "table-main table-main--leaguefixtures h-mb15 js-tablebanner-t js-tablebanner-ntb"})

data = []
rows = table_matches.find_all('tr')

for row in rows:
    utils = []
    cols = row.find_all('td')

    for element in cols:
        utils.append(element.text)
        
    data.append(utils)

# Create a DataFrame with the scraped data
df = pd.DataFrame(data, columns=["Date", "Match", "B", "C", "1", "2"])

df[['Home Team', 'Away Team']] = df['Match'].str.split('-', expand=True)

df.drop(columns=['B', 'C'], axis=1, inplace=True)
df.dropna(subset={'1'}, inplace=True)
df = df[df['1'] != '\xa0']
df.reset_index(inplace=True)
for index, row in df.iterrows():
    if row['Date'] == '\xa0' and index > 0:
        df.at[index, 'Date'] = df.at[index - 1, 'Date']


df['1'] = df['1'].astype(float)
df['2'] = df['2'].astype(float)


df['Implied_Prob_1'] = 1/df['1']
df['Implied_Prob_2'] = 1/df['2']

df['Home Team Win Probability'] = np.round(df['Implied_Prob_1']/(df['Implied_Prob_1'] + df['Implied_Prob_2']), 3)
df['Away Team Win Probability'] = np.round(df['Implied_Prob_2']/(df['Implied_Prob_1'] + df['Implied_Prob_2']), 3)

df.drop(columns = ['index','Match', '1', '2', 'Implied_Prob_1', 'Implied_Prob_2'], axis=1, inplace=True)

df.rename({'Date': 'Date and Time of Match'}, axis=1, inplace=True)


df.to_csv('/Users/jamiewelsh/Python/NBA_win_percentages/updated_table.csv', index=False)