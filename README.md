# 🔗 Web Scraper & Tiny URL Projects (Python)

This repository contains two mini projects built using Python:

1. 🌐 **Web Scraper** – Scrapes webpages for titles, headings, paragraphs, links, and images.
2. 🔗 **Tiny URL (URL Shortener)** – Converts long URLs into short, shareable links.

---

## 📁 Project 1: Web Scraper

### Description:
This is a CLI-based tool built using `requests` and `BeautifulSoup` to extract structured content from any public webpage.

### Features:
- Validate and scrape any webpage URL.
- Extract:
  - ✅ Title
  - ✅ Meta description
  - ✅ Headings (h1, h2, h3)
  - ✅ Paragraphs
  - ✅ Hyperlinks
  - ✅ Image links
- Handles errors and invalid URLs gracefully.

### How to Run:
python web_scraper.py

############## Output ######################
=== Web Scraper ===
Enter 'quit' to exit

Enter a webpage URL to scrape: https://www.python.org
Scraping website... This may take a few seconds.

============================================================
SCRAPED DATA FOR: https://www.python.org
============================================================

 Title: Welcome to Python.org

 Meta Description: The official home of the Python Programming Language

 H1 Headings (5):
  1. Functions Defined
  2. Compound Data Types
  3. Intuitive Interpretation
  4. All the Flow You’d Expect
  5. Quick & Easy to Learn

 H2 Headings (9):
  1. Get Started
  2. Download
  3. Docs
  4. Jobs
  5. Latest News
  6. Upcoming Events
  7. Success Stories
  8. Use Python for…
  9. >>> Python Software Foundation

 Paragraphs (5):
  1. Notice: While JavaScript is not essential for this website, your interaction with the content will b...
  2. The core of extensible programming is defining functions. Python allows mandatory and optional argum...
  3. Lists (known as arrays in other languages) are one of the compound data types that Python understand...
  4. Calculations are simple with Python, and expression syntax is straightforward: the operators +, -, *...
  5. Python knows the usual control flow statements that other languages speak — if, for, while and range...

 Links (10):
  1. Skip to content -> https://www.python.org#content
  2. ▼ Close -> https://www.python.org#python-network
  3. Python -> https://www.python.org/
  4. PSF -> https://www.python.org/psf/
  5. Docs -> https://docs.python.org
  6. PyPI -> https://pypi.org/
  7. Jobs -> https://www.python.org/jobs/
  8. Community -> https://www.python.org/community/
  9. ▲ The Python Network -> https://www.python.org#top
  10. No text -> https://www.python.org/

Images (1):
  1. python™ -> https://www.python.org/static/img/python-logo.png

------------------------------------------------------------
Project📁 2: Tiny URL (URL Shortener)
Description:
A simple Python-based tool that shortens long URLs using external APIs (like tinyurl.com) or local logic.
Features:
Convert long URLs into short links.
Uses requests to connect with TinyURL API (or any shortening service).
Useful for quick sharing and saving space.

run command:-python tiny_url.py

############## Output ######################
=== TinyURL Generator ===
Enter 'quit' to exit
Enter a URL to shorten:

Enter a URL to shorten: https://www.wikipedia.org/
Shortening URL...
 Original URL: https://www.wikipedia.org/
Shortened URL: https://tinyurl.com/yghajsp

Install all dependencies with:
pip install -r requirements.txt
