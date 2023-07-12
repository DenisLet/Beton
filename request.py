# import requests
# from bs4 import BeautifulSoup
#
# url = 'https://www.soccer24.com/match/KMzV9yeM/#/match-summary/match-summary'
#
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# og_description = soup.find('meta', attrs={'name': 'og:description'})
# value = og_description['content']
#
# print(value)

#
# sport_url_soc = 'https://www.soccer24.com/'
# sport_url_bb = 'https://www.basketball24.com/'
#
# print('soccer' in sport_url_soc )
# print('basket' in sport_url_bb)

x2 = ['PRE-MATCH', 'ODDS', '1', '1.29', 'X', '6.00', '2', '10.00', '1', '1.32', 'X', '6.08', '2', '9.47', 'BET365', '-', 'Click', 'to', 'see', 'if', 'you', 'qualify', 'for', 'New', 'Customer', 'offer', 'Check', 'bet365.com', 'for', 'latest', 'offers', 'and', 'details.', 'Geo-variations', 'and', 'T&Cs', 'apply.', '18+', '1xBET', '-', '100%', 'deposit', 'bonus', 'up', 'to', '€100']

print(x.index('HALF'), x.index('HALF'))