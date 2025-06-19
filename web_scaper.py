import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        print("\nPage Title:", soup.title.string if soup.title else "No title found")

        print("\nHeadings (H1):")
        for heading in soup.find_all('h1'):
            print("-", heading.text.strip())

        print("\nParagraphs:")
        for para in soup.find_all('p')[:5]:  # Print first 5 paragraphs
            print("-", para.text.strip())

        print("\nLinks:")
        for link in soup.find_all('a', href=True)[:5]:  # Print first 5 links
            print("-", link['href'])

    except Exception as e:
        print("Error:", e)

url_input = input("Enter a webpage URL to scrape: ")
scrape_website(url_input)
