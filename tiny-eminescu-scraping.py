from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin

url = "https://www.versuri.ro/artist/mihai-eminescu/"

"""
Replace with your user agent
"""
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Define the regex pattern to match the href attribute
    pattern = re.compile(r'/versuri/mihai-eminescu[^/]+/')

    # Find all 'a' tags with href matching the pattern
    matching_tags = soup.find_all('a', href=pattern)

    # Save the absolute URLs of the matching tags in a list
    list_urls = []
    for tag in matching_tags:
        relative_link = tag.get('href')
        absolute_link = urljoin(url, relative_link)
        list_urls.append(absolute_link)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def write_dataset(list_urls: list):
    # Open a text file to write parsed lines on web pages
    f = open("tiny-eminescu.txt", "w")

    # Parse each URL and save poetry content in the text file
    for i in range(len(list_urls)):
        url = list_urls[i]
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the HTML content of the webpage and write it to txt file
            soup = BeautifulSoup(response.text, 'html.parser')
            
            matching_tags = soup.find_all('p')

            h1_tag = soup.find('h1')

            f.write(h1_tag.get_text().split("-")[0])
            f.write("\n-\n\n")

            for item in range(len(matching_tags)):
                matching_tags[item] = matching_tags[item].prettify().replace("<p>", "").replace("</p>", "").replace("<br/>", "").replace("</br>", "").replace("<br>", "").split("\n")

                filtered_list = [elem.strip() for elem in matching_tags[item] if elem != '']

                for elem in filtered_list:
                    f.write(elem)
                    f.write("\n")

        f.write("\n\n\n")
    f.close()

write_dataset(list_urls)