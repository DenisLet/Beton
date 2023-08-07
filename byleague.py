from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
linka = 'https://www.soccer24.com/match/bgJJ0Bq4/#/match-summary/match-summary'
# def create_div_dict(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#
#         # Go to the URL
#         page.goto(url)
#
#         # Get the HTML content of the page
#         html_content = page.content()
#
#         # Close the browser after getting the HTML content
#         browser.close()
#
#     # Create an empty dictionary to store the results
#     div_dict = {}
#
#     # Parse the HTML using BeautifulSoup
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     # Find all elements with class 'event__header'
#     event_headers = soup.find_all('div', class_='event__header')
#
#     # Iterate through 'event__header' elements
#     for header in event_headers:
#         # Find all sibling elements with id starting with 'g_1'
#         sibling_elements = header.find_next_siblings('div', id=lambda x: x and x.startswith('g_1'))
#
#         # Get the text content of the sibling elements
#         values = [el.get_text().split() for el in sibling_elements]
#
#         # If matching elements are found, add corresponding key-value pairs to the dictionary
#         if values:
#             div_dict[header.get_text(separator=' ')] = values
#
#     return div_dict
#
# # Replace 'your_url_here' with the actual URL of your webpage
# url = 'https://www.soccer24.com/'
# result_dict = create_div_dict(url)
#
# for i,j in result_dict.items():
#     print(i,j)


import requests

resp = requests.get(linka)
content = resp.text

soup = BeautifulSoup(content, 'html.parser')
hidden_elements = soup.find_all(lambda tag: tag.has_attr('style') and 'display:none' in tag['style'] or tag.has_attr('hidden'))
hidden_text = [element.get_text() for element in hidden_elements]
for text in hidden_text:
    print(text.strip())

heading = soup.find('meta', attrs={'name': 'og:description'})
text_value = heading['content']
print(text_value)

print(resp)

