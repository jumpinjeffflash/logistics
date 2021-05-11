import pandas as pd
import yfinance as yf
import streamlit as st
import requests

from pygooglenews import GoogleNews

gn = GoogleNews(country = 'USA')

from bs4 import BeautifulSoup
header = {"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/33.0 GoogleChrome/10.0"}

st.write("""
# Company Profiler
""")

# This is where users pick the company they want to look at. It's defaulted to XPO Logistics:

option = st.sidebar.selectbox("Please make your selection:", ('XPO', 'RoadRunner', 'CH Robinson', 'Uber', 'Ryder System', 'FedEx', 'ShipMonk', 'ShipBob'), 0)

# XPO LOGISTICS

if option == 'XPO':

    st.image('https://www.voiteq.com/wp-content/uploads/2020/01/XPO-Logo-Print-Use_CMYK_RedBlack.jpg', width=400)
    
    tickerSymbol = 'XPO'
    
# Fetch the data on this ticker
    
    tickerData = yf.Ticker(tickerSymbol)

# Info on XPO LOGISTICS from Yahoo Finance
    
    st.write("""## Company Details (from YahooFinance)""")
    
    st.write(""" #### Total Employees:""")
    tickerData.info['fullTimeEmployees']
                    
    st.write(""" #### Headquarters:""")    
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']

# Google News about XPO (last 12 hours)
        
    st.write("""### Latest XPO Logistics news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, when = '12h')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"xpo logistics"'))
    
    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)

# XPO: This part starts Beautiful Soup
    # This fetches TrustPilot Review scores for XPO

    url = (f'https://www.trustpilot.com/review/xpo.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    # REVIEW SCORE
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:47]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")
     
# XPO: IOS APP REVIEW SCORE
    # This grabs the DriveXPO review score from IOS STORE:
    
    url = (f'https://apps.apple.com/us/app/drive-xpo-find-book-loads/id1268107798')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    
    ios_app_score = soup.find('div', class_='we-customer-ratings__averages')
    st.write("""### iOS Store: Drive XPO App review score (out of 5): """)
    ios_app_score_string = str(ios_app_score)
    ios_app_score_total = ios_app_score_string[96:99]
    st.write(ios_app_score_total)
    
    ios_app_reviews = soup.find('div', class_='we-customer-ratings__count small-hide medium-show')
    ios_app_reviews_string = str(ios_app_reviews)
    ios_app_reviews_total = ios_app_reviews_string[63:73]
    st.write(ios_app_reviews_total)
        
# XPO: GOOGLE STORE APP REVIEW SCORE
    # This grabs the DriveXPO review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.xpo.DriveXPO&hl=en_US&gl=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: Drive XPO App review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[47:58]
    st.write(android_app_reviews_total)
    
# Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # This fetches Indeed.com review score & number of reviews   
    
    url = (f'https://www.indeed.com/cmp/Xpo-Logistics/reviews')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee review score (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
    
# This creates the list that populates the table in the dashboard
# It looks for all the reviews on the first page

    st.write("""### Latest employee reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)

# XPO: STOCK MARKET PRICES
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
# Fetch the historical prices for this ticker
    
    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### XPO Logistics Stock Price (NYSE: XPO)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
# Latest Stockmarket Analyst Recommendations (most recent 5)
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    # get recommendation data for ticker
    xpo_recos = tickerData.recommendations
    st.write(xpo_recos.sort_index(ascending = False).head(5))
    
# XPO: StockTwits
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/XPO.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

# End of XPO Logistics
                
#
# ROADRUNNER TRANSPORTATION
#

if option == 'RoadRunner':

    st.image("https://investors.rrts.com/sites/g/files/knoqqb33421/themes/site/nir_pid2363/dist/images/logo.png")
    
# Fetch the data on this ticker
    
    tickerSymbol = 'RRTS'

    tickerData = yf.Ticker(tickerSymbol)
    
# Info on RoadRunner from Yahoo Finance

    st.write("""## Company Details (from YahooFinance)""")
    
    st.write(""" #### Total Employees:""")
    tickerData.info['fullTimeEmployees']
                    
    st.write(""" #### Headquarters:""")
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']
    
# Google News about RoadRunner (since January, 2021)
    
    st.write("""### Latest RoadRunner news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-1-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"roadrunner transportation"'))

# ROADRUNNER REVIEWS:

    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)

# ROADRUNNER DOESN'T HAVE ANY TRUSTPILOT REVIEW SCORES

    st.write("""### TrustPilot review score (out of 5) : """)
    st.write("This company has no TrustPilot reviews")
    
# ROADRUNNER APP: HAUL NOW IS ONLY ON ANDROID
    
    url = (f'https://apps.apple.com/us/app/drive-xpo-find-book-loads/id1268107798')
    
    st.write("""### iOS Store: Haul NOW App review score (out of 5): """)
    st.write("Haul NOW is only available on Android")
    
# ROADRUNNER GOOGLE STORE APP REVIEW SCORE
    # This grabs the ROADRUNNER review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.roadrunner.freightLTL')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: RoadRunner Haul NOW review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[45:55]
    st.write(android_app_reviews_total)
    
# Indeed heading for ROADRUNNER
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
      
# This part starts Beautiful Soup. It also grabs the rewiew score and number of reviews
        
    url = (f'https://www.indeed.com/cmp/Roadrunner-Transportation-Systems/reviews?fcountry=ALL')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee Review Score (out of 5) via Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])

# ROADRUNNER This creates the list that populates the table in the dashboard
# It looks for all the reviews on the first page

    st.write("""### Latest Employee Reviews (via Indeed.com): """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)
    
# Yahoo Finance heading
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
# Fetch the historical prices for this ticker

    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### Roadrunner Transportation Systems (OTCMKTS: RRTS)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    
# Get Analyst recommendation data for ticker
    
    st.write(tickerData.recommendations)
    
# ROADRUNNER: StockTwits
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/RRTS.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])    

### End of RoadRunner
        
        
#
# CH ROBINSON
#

if option == 'CH Robinson':

    st.image("https://inmotionglobal.com/assets/images/CHRobinson_FullColorFlat_HiRes.jpg")        

# get data on this ticker

    tickerSymbol = 'CHRW'
    
    tickerData = yf.Ticker(tickerSymbol)
        
# info on the company
    
    st.write(""" #### Total Employees:""")
    tickerData.info['fullTimeEmployees']
                    
    st.write(""" #### Headquarters:""")
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']
        
# Google News about CH ROBINSON (last 24 hours)
    
    st.write("""### Latest RoadRunner news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, when = '24h')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"ch robinson"'))    
      
# CH ROBINSON REVIEWS:

    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)           
        
# This fetches TRUST PILOT REVIEW SCORES for CH ROBINSON

    url = (f'https://www.trustpilot.com/review/chrobinson.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    # REVIEW SCORE
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:52]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")        
        
# CH ROBINSON: IOS APP REVIEW SCORE
    # This grabs the NAVISPHERE review score from IOS STORE:
    
    url = (f'https://apps.apple.com/us/app/navisphere-carrier/id1089613477')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    
    ios_app_score = soup.find('div', class_='we-customer-ratings__averages')
    st.write("""### iOS Store: CH Robinson Navisphere Carrier App review score (out of 5): """)
    ios_app_score_string = str(ios_app_score)
    ios_app_score_total = ios_app_score_string[96:99]
    st.write(ios_app_score_total)
    
    ios_app_reviews = soup.find('div', class_='we-customer-ratings__count small-hide medium-show')
    ios_app_reviews_string = str(ios_app_reviews)
    ios_app_reviews_total = ios_app_reviews_string[63:73]
    st.write(ios_app_reviews_total)       
        
# CH ROBINSON: GOOGLE STORE APP REVIEW SCORE
    # This grabs the Navisphere review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.chrobinson.navispherecarrier&hl=en_US&gl=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: CH Robinson Navisphere Carrier App review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[45:56]
    st.write(android_app_reviews_total)        
        
# Indeed heading for CH ROBINSON
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
      
    # This part initializes Beautiful Soup. It also grabs the rewiew score and number of reviews
        
    url = (f'https://www.indeed.com/cmp/C.h.-Robinson/reviews?fcountry=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee Review Score (out of 5) via Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
  
    # This creates the list that populates the table in the dashboard
    # It looks for all the reviews on the first page

    st.write("""### Latest Employee Reviews (via Indeed.com): """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)
    
# Yahoo Finance heading
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
    # Fetch the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### Roadrunner Transportation Systems (NASDAQ: CHRW)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    
# Get Analyst recommendation data for ticker (most recent 5)

    chrw_recos = tickerData.recommendations
    st.write(chrw_recos.sort_index(ascending = False).head(5))
    
    # CH ROBINSON: THIS IS FOR STOCKTWITS
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/CHRW.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])          

# End of CH Robinson

#
# Ryder System, Inc.
#
        
if option == 'Ryder System':

# This is the Ryder logo:
    st.image("https://logos-download.com/wp-content/uploads/2020/06/Ryder_Logo.png", width = 200)      
        
# Fetch data on this ticker    

    tickerSymbol = 'R'
    
    tickerData = yf.Ticker(tickerSymbol)

# info on Ryder Systems from Yahoo Finance
    
    st.write("""## Company Details (from YahooFinance)""")
    
    st.write(""" #### Total Employees:""")
    tickerData.info['fullTimeEmployees']
                    
    st.write(""" #### Headquarters:""")    
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']      
        
# Google News about Ryder System (since May, 2021)

    st.write("""### Latest Ryder System news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    st.write("""
    ### Latest News (via Google)
    """)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-5-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"ryder system"'))    
    
    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)        
        
# This fetches Ryder System TrustPilot Review Scores
    
    url = (f'https://www.trustpilot.com/review/ryder.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')    
    
    # SHIPBOB REVIEW SCORE
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:52]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")    
        
        
# Ryder: IOS APP REVIEW SCORE
    # This grabs the App review score from IOS STORE:
    
    url = (f'https://apps.apple.com/us/app/coop-by-ryder/id1476769173')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    
    ios_app_score = soup.find('div', class_='we-customer-ratings__averages')
    st.write("""### iOS Store: COOP by Ryder App review score (out of 5): """)
    ios_app_score_string = str(ios_app_score)
    ios_app_score_total = ios_app_score_string[96:99]
    st.write(ios_app_score_total)
    
    ios_app_reviews = soup.find('div', class_='we-customer-ratings__count small-hide medium-show')
    ios_app_reviews_string = str(ios_app_reviews)
    ios_app_reviews_total = ios_app_reviews_string[63:73]
    st.write(ios_app_reviews_total)
    
    
#Ryder: GOOGLE STORE APP SCORE
    # This grabs the Uber Freight review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.ryder.coop&hl=en_US&gl=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: COOP by Ryder App review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[45:55]
    st.write(android_app_reviews_total)        
        
# Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # This fetches Indeed.com review score and number of reviews   
    
    url = (f'https://www.indeed.com/cmp/Ryder-System-Inc./reviews')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee review score (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
 
    ### This creates the list that populates the table in the dashboard
    ### It looks for all the reviews on the first page

    st.write("""### Latest employee reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)

# RYDER: STOCK MARKET PRICES
    
    # Yahoo Finance heading
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
    #get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### Ryder System Stock Price (NYSE: R)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
    # Latest Stockmarket Analyst Recommendations (most recent 5)
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    # get recommendation data for ticker
    ryder_recos = tickerData.recommendations
    st.write(ryder_recos.sort_index(ascending = False).head(5))
    
# RYDER: StockTwits
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/R.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

### End of Ryder Systems        
              
#    
# UBER FREIGHT
#

if option == 'Uber':

    st.image('https://roadys.com/wp-content/uploads/2018/12/uber-freight-logo-for-light-background.png', width=400)
    
# Fetch data on this ticker
    
    tickerSymbol = 'UBER'
    
    tickerData = yf.Ticker(tickerSymbol)

# info on UBER from Yahoo Finance
    
    st.write("""## Company Details (from YahooFinance)""")
    
    st.write(""" #### Total Uber Employees:""")
    tickerData.info['fullTimeEmployees']
    
    st.write(""" #### Headquarters:""")    
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']

# Google News about Uber Freight (since March, 2021)
        
    st.write("""### Latest Uber Freight news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-3-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"uber freight"'))
    
    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)

# Uber: This part starts Beautiful Soup
    
    #This fetches TRUST PILOT REVIEW SCORES for Uber Freight
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write("No Freight reviews available")
    
    
# Uber: IOS APP REVIEW SCORE
    # This grabs the UBER FREIGHT review score from IOS STORE:
    
    url = (f'https://apps.apple.com/us/app/uber-freight/id1183931851')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    
    ios_app_score = soup.find('div', class_='we-customer-ratings__averages')
    st.write("""### iOS Store: Uber Freight App review score (out of 5): """)
    ios_app_score_string = str(ios_app_score)
    ios_app_score_total = ios_app_score_string[96:99]
    st.write(ios_app_score_total)
    
    ios_app_reviews = soup.find('div', class_='we-customer-ratings__count small-hide medium-show')
    ios_app_reviews_string = str(ios_app_reviews)
    ios_app_reviews_total = ios_app_reviews_string[63:75]
    st.write(ios_app_reviews_total)
    
    
# Uber: GOOGLE STORE UBER FREIGHT APP SCORE
    # This grabs the Uber Freight review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.ubercab.freight&hl=en_US&gl=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: Uber Freight App review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[47:58]
    st.write(android_app_reviews_total)
    
# Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # This fetches Indeed.com review score and number of reviews   
    
    url = (f'https://www.indeed.com/cmp/Uber-Freight/reviews')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Uber Freight employee review score (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
 
    ### This creates the list that populates the table in the dashboard
    ### It looks for all the reviews on the first page

    st.write("""### Latest Uber Freight employee reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)
    
# UBER: STOCK MARKET PRICES
    
    # Yahoo Finance heading
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
    # Fetch the historical prices for this ticker
    
    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### XPO Logistics Stock Price (NYSE: UBER)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
    # Latest Stockmarket Analyst Recommendations (most recent 5)
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    # get recommendation data for ticker
    uber_recos = tickerData.recommendations
    st.write(uber_recos.sort_index(ascending = False).head(5))
    
# UBER: THIS IS FOR STOCKTWITS
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/UBER.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

# End of Uber (Freight)        
        
#
# FEDEX CORPORATION
#

if option == 'FedEx':

    st.image('https://logo.clearbit.com/fedex.com')
    
# Fetch data on this ticker
    
    tickerSymbol = 'FDX'
   
    tickerData = yf.Ticker(tickerSymbol)

    #info on FedEx from Yahoo Finance
    
    st.write("""## Company Details (from YahooFinance)""")
    
    st.write(""" #### Total FedEx Employees:""")
    tickerData.info['fullTimeEmployees']
                    
    st.write(""" #### Headquarters:""")    
    city = tickerData.info['city']
    state = tickerData.info['state']
    st.write(city+ ", "+ state)
        
    st.write(""" #### Business Description:""")
    tickerData.info['longBusinessSummary']

# Google News about FedEx Freight (Since March, 2021)
        
    st.write("""### Latest FedEx Freight news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-3-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"fedex freight"'))
    
    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.pngkey.com/png/detail/267-2675337_appstore-playstore-apple-android-windows-logo-hd.png', width=100)

# FEDEX: This part starts Beautiful Soup
    
    #This fetches TRUST PILOT REVIEW SCORES for FedEx

    url = (f'https://www.trustpilot.com/review/www.fedex.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    # REVIEW SCORE
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:50]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")
    
    
# FEDEX: IOS APP REVIEW SCORE
    # This grabs the review score from IOS STORE:
    
    url = (f'https://apps.apple.com/us/app/fedex-mobile/id1010729050')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    
    ios_app_score = soup.find('div', class_='we-customer-ratings__averages')
    st.write("""### iOS Store: FedEx Mobile App review score (out of 5): """)
    ios_app_score_string = str(ios_app_score)
    ios_app_score_total = ios_app_score_string[96:99]
    st.write(ios_app_score_total)
    
    ios_app_reviews = soup.find('div', class_='we-customer-ratings__count small-hide medium-show')
    ios_app_reviews_string = str(ios_app_reviews)
    ios_app_reviews_total = ios_app_reviews_string[63:77]
    st.write(ios_app_reviews_total)
    
    
# FEDEX: GOOGLE STORE APP SCORE
    # This grabs the review score from GOOGLE PLAY:
    
    url = (f'https://play.google.com/store/apps/details?id=com.fedex.ida.android&hl=en_US&gl=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    android_app_score = soup.find('div', class_='BHMmbe')
    st.write("""### Android Store: FedEx Mobile App review score (out of 5): """)
    android_app_score_string = str(android_app_score)
    android_app_score_total = android_app_score_string[66:70]
    st.write(android_app_score_total)
    
    android_app_reviews = soup.find('span', class_= 'AYi5wd TBRnV')
    android_app_reviews_string = str(android_app_reviews)
    android_app_reviews_total = android_app_reviews_string[45:59]
    st.write(android_app_reviews_total)
    
# Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # This fetches Indeed.com review score and number of reviews   
    
    url = (f'https://www.indeed.com/cmp/FedEx-Freight/reviews?fcountry=US')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### FedEx Freight employee review score (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
 
    ### This creates the list that populates the table in the dashboard
    ### It looks for all the reviews on the first page

    st.write("""### Latest FedEx Freight employee reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)
    
# FEDEX: STOCK MARKET PRICES
    
    # Yahoo Finance heading
    
    st.write("""## Voice of the investor: Stock price trend & sentiment""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e4/YahooFinanceLogo.png', width=100)
    
    #get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start='2010-1-1')

    st.write("""
    ### FedEx Stock Price (NYSE:FDX)
    """)
    st.line_chart(tickerDf.Close)

    st.write(""" #### Previous closing price (USD):""")
    tickerData.info['previousClose']
    
    # Latest Stockmarket Analyst Recommendations (most recent 5)
    
    st.write("""
    ### Latest Stockmarket Analyst Recommendations
    """)
    # get recommendation data for ticker
    fdx_recos = tickerData.recommendations
    st.write(fdx_recos.sort_index(ascending = False).head(5))
    
# FDX: StockTwits
    
    st.write("""
    ### Latest Stockmarket-related Insights & Gossip (via StockTwits)
    """)
    
    st.image('https://www.socialmarketanalytics.com/wp-content/uploads/2020/02/logo.png', width=150)
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/FDX.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])    
    
# End of FedEx (Freight) 

#        
# SHIPMONK        
#

if option == 'ShipMonk':
    
    st.image("https://iem4i1awkgx4628vb7ghf4f2-wpengine.netdna-ssl.com/wp-content/uploads/2018/01/shipmonk-logo-2.png")
    
    st.write("""## Company Details (from GetLatka.com)""")
    
    st.write("""#### Est'd Employees:""")
    st.write("""1,000""")
    
    st.write("""#### Headquarters:""")   
    st.write("""Miami, FL""")   
    
    st.write("""#### Est'd 2020 Revenue:""")
    st.write("""$100m """)
 
    st.write("""#### Total Funding: """)
    st.write("""$300m""")
  
    st.write("""#### Company Description: """)
    st.write("""ShipMonk is a cloud-based platform that develops and provides supply chain management solutions for the E-commerce sector.""")
    
# Google News about SHIPMONK (since January, 2021)
   
    st.write("""### Latest ShipMonk news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-1-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"shipmonk"'))

    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.citypng.com/public/uploads/preview/-11597191761n5ghafjnrt.png', width=100)
    
    # This part starts Beautiful Soup
    
    #This fetches TRUST PILOT REVIEW SCORES

    url = (f'https://www.trustpilot.com/review/shipmonk.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')

    # SHIPMONK REVIEW SCORE
    
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:52]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")
    
# SHIPMONK: This grabs the App review score from Shopify
    
    url = (f'https://apps.shopify.com/shipmonk')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'ui-star-rating__text'})
    
    # this shows the app score
    app_review_score = soup.find_all('span', class_='ui-star-rating__rating')
    st.write("""### Shopify Store: Order Fulfillment App review score (out of 5): """)
    st.write(app_review_score[0].contents[0])

    # this shows total reviews
    app_reviews = soup.find(attrs={"href": "#reviews"})
    app_reviews_string = str(app_reviews)
    app_review_total = app_reviews_string[37:49]
    st.write(app_review_total)
    
# ShipMonk Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""") 
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # SHIPMONK: This part initializes Beautiful Soup
    # It also grabs the rewiew score and number of reviews   
    
    url = (f'https://www.indeed.com/cmp/Shipmonk/reviews?fcountry=ALL')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee review scores (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
  
    # This creates the list that populates the table in the dashboard. It looks for all the reviews on the first page

    st.write("""### Latest Employee Reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)

# End of ShipMonk    
    
##        
# SHIPBOB      
##

if option == 'ShipBob':
    
    st.image('https://mma.prnewswire.com/media/522416/ShipBob_Logo.jpg?p=publish', width= 200)
    
    st.write("""## Company Details (from Owler)""")
    
    st.write("""#### Est'd Employees:""")
    st.write("""900""")
    
    st.write("""#### Headquarters:""")   
    st.write("""Chicago, IL""")   
    
    st.write("""#### Est'd 2020 Revenue:""")
    st.write("""$35m """)
 
    st.write("""#### Total Funding: """)
    st.write("""$130m """)
  
    st.write("""#### Company Description: """)
    st.write("""ShipBob provides software that offers optimized shipping and inventory management solutions for merchants and e-commerce businesses.""")
    
# Google News about SHIPBOB (since May, 2021)
       
    st.write("""### Latest ShipMonk news (via Google News)""")
    st.image('https://iconape.com/wp-content/png_logo_vector/google-news.png', width=50)
    
    def get_titles(search):
        stories = []
        search = gn.search(search, from_= '2021-5-1')
        newsitem = search['entries']
        for item in newsitem:
            story = {
                'title': item.title,
                'published':item.published,
                'link': item.link
            }
            stories.append(story)
        return stories
    
    st.write(get_titles('allintitle:"shipbob"'))

    st.write("""## Voice of the customer: TrustPilot & App review scores""")
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Trustpilot_logo.png', width=100)
    st.image('https://www.citypng.com/public/uploads/preview/-11597191761n5ghafjnrt.png', width=100)
    
    # This part starts Beautiful Soup
    
    #This fetches TRUST PILOT REVIEW SCORES

    url = (f'https://www.trustpilot.com/review/shipbob.com')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')    
    
    # SHIPBOB REVIEW SCORE
    trustpilot_review_score = soup.find('div', class_='star-rating')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_score_string = str(trustpilot_review_score)
    trustpilot_review_score_final = trustpilot_review_score_string[36:56]
    
    st.write("""### TrustPilot review score (out of 5) : """)
    st.write(trustpilot_review_score_final)
    
    # NUMBER OF REVIEWS
    trustpilot_review_total = soup.find('span', class_='headline__review-count')
    
    # convert to a string so we can slice the score:
    
    trustpilot_review_total_string = str(trustpilot_review_total)
    trustpilot_review_total_final = trustpilot_review_total_string[36:40]

    st.write((trustpilot_review_total_final), """ratings""")
    
# SHIPBOB: This grabs the App review score from Shopify
  
    url = (f'https://apps.shopify.com/shipbob/reviews')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'ui-star-rating__text'})
    
    # this shows the app score
    review_score = soup.find('span', class_='ui-star-rating__rating')
    st.write("""### Shopify Store: Order Fulfillment App review score (out of 5): """)
    review_score_string = str(review_score)
    review_score_final = review_score_string[36:40]
    st.write(review_score_final)

    # this shows total reviews
    app_reviews = soup.find('div', class_='grid__item gutter-bottom')
    app_reviews_string = str(app_reviews)
    app_review_total = app_reviews_string[53:64]
    st.write(app_review_total)
    
# ShipBob Indeed heading
    
    st.write("""## Voice of the employee: Indeed.com review scores""") 
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Indeed_logo.svg/320px-Indeed_logo.svg.png', width=100)
    
    # SHIPBOB: This part initializes Beautiful Soup
    # It also grabs the rewiew score and number of reviews   
    
    url = (f'https://www.indeed.com/cmp/Shipbob/reviews')
    
    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find("div", { "id" : 'cmp-container'})
    
    review_score = soup.find_all('div', class_='cmp-OverallCompanyRating-value')
    st.write("""### Employee review scores (out of 5) from Indeed.com: """)
    st.write(review_score[0].contents[0])
    
    total_reviews = soup.find_all('div', class_='cmp-OverallCompanyRating-note')
    st.write(total_reviews[0].contents[0])
  
    # This creates the list that populates the table in the dashboard. It looks for all the reviews on the first page

    st.write("""### Latest Employee Reviews from Indeed.com: """)
    
    df = pd.DataFrame({'review_title': [], 'review': [], 'author': [], 'rating':[]})
    
    for i in range(0,1):        
        elems = results.find_all(class_='cmp-Review-container')
         
        for elem in elems:
            title = elem.find(attrs = {'class':'cmp-Review-title'})
            review = elem.find('div', {'class': 'cmp-Review-text'})
            author = elem.find(attrs = {'class':'cmp-Review-author'})
            rating = elem.find(attrs = {'class':'cmp-ReviewRating-text'})
            df = df.append(
                 {'review_title': title.text,
                  'review': review.text,
                  'author': author.text,
                  'rating': rating.text
            }, ignore_index=True)
                    
    st.write(df)

### End of ShipBob