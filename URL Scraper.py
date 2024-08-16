import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_urls(domain):
    """
    Fetches all URLs from the given domain.
    
    Args:
        domain (str): The domain from which to fetch URLs.
    
    Returns:
        set: A set of URLs found on the domain.
    """
    logging.info(f"Fetching URLs from: {domain}")
    urls = set()
    
    try:
        response = requests.get(domain)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch URLs. Error: {e}")
        return urls
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting URLs from <a> tags
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.startswith('http'):  # Absolute URLs
            urls.add(url)
        else:  # Relative URLs
            urls.add(urljoin(domain, url))
    
    logging.info(f"Found {len(urls)} URLs on {domain}")
    return urls

def save_urls_to_file(urls, filename):
    """
    Saves the collected URLs to a text file.
    
    Args:
        urls (set): A set of URLs to be saved.
        filename (str): The name of the file to save the URLs to.
    """
    if not urls:
        logging.warning("No URLs to save.")
        return
    
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        logging.info(f"All URLs saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save URLs to {filename}. Error: {e}")

def main():
    while True:
        domain = input("Enter the URL of the domain to scrape (or type 'e' to quit): ").strip()
        
        if domain.lower() == 'e':
            logging.info("Exiting the script.")
            break
        
        if not domain.startswith('http'):
            domain = 'https://' + domain
        
        # Ensure the domain ends with a '/'
        if not domain.endswith('/'):
            domain += '/'
        
        # Scrape URLs and save to file
        urls = fetch_urls(domain)
        
        if urls:
            # Generate a filename based on the domain
            filename = os.path.join(os.getcwd(), f"urls_{domain.replace('https://', '').replace('http://', '').replace('/', '')}.txt")
            save_urls_to_file(urls, filename)
        else:
            logging.info("No URLs found to save.")

if __name__ == "__main__":
    main()
