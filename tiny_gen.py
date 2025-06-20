from typing import Optional
from urllib.parse import urlparse

import requests


class URLShortener:
    def __init__(self, timeout: int = 10):
        
        self.api_base = "http://tinyurl.com/api-create.php"
        self.timeout = timeout

    def is_valid_url(self, url: str) -> bool:
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def shorten_url(self, long_url: str) -> Optional[str]:
       
        if not long_url or not isinstance(long_url, str):
            raise ValueError("URL must be a non-empty string")

        if not self.is_valid_url(long_url):
            raise ValueError("Invalid URL format")

        try:
            response = requests.get(
                self.api_base, params={"url": long_url}, timeout=self.timeout
            )
            response.raise_for_status()

            shortened_url = response.text.strip()

            # Validate the returned shortened URL
            if self.is_valid_url(shortened_url):
                return shortened_url
            else:
                raise ValueError("Invalid response from TinyURL API")

        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to TinyURL API")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")


def main():
    shortener = URLShortener()

    print("=== TinyURL Generator ===")
    print("Enter 'quit' to exit\n")

    while True:
        try:
            url_input = input("Enter a URL to shorten: ").strip()

            if url_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not url_input:
                print("Please enter a valid URL.\n")
                continue

            print("Shortening URL...")
            shortened = shortener.shorten_url(url_input)

            print(f" Original URL: {url_input}")
            print(f"Shortened URL: {shortened}\n")

        except ValueError as e:
            print(f" Validation Error: {e}\n")
        except (TimeoutError, ConnectionError, RuntimeError) as e:
            print(f" Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled. Goodbye!")
            break
        except Exception as e:
            print(f" Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
