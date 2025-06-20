import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class WebScraper:

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def is_valid_url(self, url: str) -> bool:
       
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
       
        if not self.is_valid_url(url):
            raise ValueError("Invalid URL format")

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()

                # Check if content is HTML
                content_type = response.headers.get("content-type", "").lower()
                if "html" not in content_type:
                    raise ValueError("URL does not point to an HTML page")

                return BeautifulSoup(response.text, "html.parser")

            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    raise TimeoutError("Request timed out after multiple attempts")
                time.sleep(1)  # Wait before retry
            except requests.exceptions.ConnectionError:
                if attempt == self.max_retries - 1:
                    raise ConnectionError("Failed to connect to the website")
                time.sleep(1)
            except requests.exceptions.HTTPError as e:
                raise RuntimeError(f"HTTP error occurred: {e}")

    def extract_title(self, soup: BeautifulSoup) -> str:
       
        title_tag = soup.find("title")
        return title_tag.get_text().strip() if title_tag else "No title found"

    def extract_headings(
        self, soup: BeautifulSoup, heading_level: str = "h1", limit: int = 10
    ) -> List[str]:
        
        headings = soup.find_all(heading_level)
        return [h.get_text().strip() for h in headings[:limit] if h.get_text().strip()]

    def extract_paragraphs(self, soup: BeautifulSoup, limit: int = 5) -> List[str]:
        
        paragraphs = soup.find_all("p")
        return [
            p.get_text().strip() for p in paragraphs[:limit] if p.get_text().strip()
        ]

    def extract_links(
        self, soup: BeautifulSoup, base_url: str, limit: int = 10
    ) -> List[Tuple[str, str]]:
       
        links = []
        link_tags = soup.find_all("a", href=True)

        for link in link_tags[:limit]:
            href = link["href"]
            text = link.get_text().strip() or "No text"

            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)
            links.append((text, absolute_url))

        return links

    def extract_images(
        self, soup: BeautifulSoup, base_url: str, limit: int = 5
    ) -> List[Tuple[str, str]]:
       
        images = []
        img_tags = soup.find_all("img", src=True)

        for img in img_tags[:limit]:
            src = img["src"]
            alt = img.get("alt", "No alt text")

            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, src)
            images.append((alt, absolute_url))

        return images

    def scrape_website(
        self, url: str, options: Dict[str, int] = None
    ) -> Dict[str, any]:
       
        if options is None:
            options = {
                "headings_limit": 10,
                "paragraphs_limit": 5,
                "links_limit": 10,
                "images_limit": 5,
            }

        soup = self.get_page_content(url)
        if not soup:
            return {}

        scraped_data = {
            "url": url,
            "title": self.extract_title(soup),
            "headings": {
                "h1": self.extract_headings(
                    soup, "h1", options.get("headings_limit", 10)
                ),
                "h2": self.extract_headings(
                    soup, "h2", options.get("headings_limit", 10)
                ),
                "h3": self.extract_headings(
                    soup, "h3", options.get("headings_limit", 10)
                ),
            },
            "paragraphs": self.extract_paragraphs(
                soup, options.get("paragraphs_limit", 5)
            ),
            "links": self.extract_links(soup, url, options.get("links_limit", 10)),
            "images": self.extract_images(soup, url, options.get("images_limit", 5)),
            "meta_description": None,
        }

        # Extract meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            scraped_data["meta_description"] = meta_desc.get("content", "").strip()

        return scraped_data


def display_scraped_data(data: Dict[str, any]) -> None:

    print(f"\n{'=' * 60}")
    print(f"SCRAPED DATA FOR: {data['url']}")
    print(f"{'=' * 60}")

    print(f"\n Title: {data['title']}")

    if data["meta_description"]:
        print(f"\n Meta Description: {data['meta_description']}")

    # Display headings
    for level in ["h1", "h2", "h3"]:
        headings = data["headings"][level]
        if headings:
            print(f"\n {level.upper()} Headings ({len(headings)}):")
            for i, heading in enumerate(headings, 1):
                print(f"  {i}. {heading}")

    # Display paragraphs
    if data["paragraphs"]:
        print(f"\n Paragraphs ({len(data['paragraphs'])}):")
        for i, para in enumerate(data["paragraphs"], 1):
            preview = para[:100] + "..." if len(para) > 100 else para
            print(f"  {i}. {preview}")

    # Display links
    if data["links"]:
        print(f"\n Links ({len(data['links'])}):")
        for i, (text, url) in enumerate(data["links"], 1):
            text_preview = text[:50] + "..." if len(text) > 50 else text
            print(f"  {i}. {text_preview} -> {url}")

    # Display images
    if data["images"]:
        print(f"\nImages ({len(data['images'])}):")
        for i, (alt, url) in enumerate(data["images"], 1):
            print(f"  {i}. {alt} -> {url}")


def main():
    scraper = WebScraper()

    print("=== Web Scraper ===")
    print("Enter 'quit' to exit\n")

    while True:
        try:
            url_input = input("Enter a webpage URL to scrape: ").strip()

            if url_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not url_input:
                print("Please enter a valid URL.\n")
                continue

            print("Scraping website... This may take a few seconds.")

            # Custom options for extraction limits
            options = {
                "headings_limit": 10,
                "paragraphs_limit": 5,
                "links_limit": 10,
                "images_limit": 5,
            }

            scraped_data = scraper.scrape_website(url_input, options)

            if scraped_data:
                display_scraped_data(scraped_data)
            else:
                print("Failed to scrape the website.")

            print("\n" + "-" * 60)

        except ValueError as e:
            print(f"Validation Error: {e}\n")
        except (TimeoutError, ConnectionError, RuntimeError) as e:
            print(f" Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
