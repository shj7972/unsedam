import requests
import sys

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"SUCCESS: {url} is accessible.")
            return True
        else:
            print(f"FAILED: {url} returned status code {response.status_code}.")
            return False
    except Exception as e:
        print(f"ERROR: Could not access {url}. Error: {e}")
        return False

if __name__ == "__main__":
    base_url = "http://localhost:8000"
    urls_to_check = [
        "/",
        "/about",
        "/faq",
        "/privacy",
        "/terms",
        "/sitemap.xml",
        "/robots.txt"
    ]
    
    all_success = True
    for path in urls_to_check:
        if not check_url(base_url + path):
            all_success = False
            
    if all_success:
        print("\nAll pages are working correctly!")
        sys.exit(0)
    else:
        print("\nSome pages failed the check.")
        sys.exit(1)
