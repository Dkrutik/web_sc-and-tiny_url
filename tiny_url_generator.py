import requests

def shorten_url(long_url):
    try:
        api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            print("Shortened URL:", response.text)
        else:
            print("Failed to shorten URL.")
    except Exception as e:
        print("Error:", e)

url = input("Enter a long URL to shorten: ")
shorten_url(url)
