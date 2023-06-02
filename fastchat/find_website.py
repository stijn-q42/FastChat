import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text.replace("\n", " ")

def fetch_readable_html(url): 
    response = requests.get(url)

    if response.status_code != 200:
        return None

    raw_body = response.text
    clean_text = extract_text_from_html(raw_body)

    # print(clean_text)

    return clean_text

def fetch_link_for_keywords_google(keywords):
    base_url = 'http://www.google.com/search'

    query_params = {
        'q': keywords.replace("biography", ""),
        'btnI': ''
    }

    response_redirect = requests.get(base_url, params=query_params)

    # For fallbacking
    query_params_google = {
        'q': keywords,
    }
    response_google = requests.get(base_url, params=query_params_google)

    if response_redirect.status_code != 200 or not response_redirect.url:
        return [response_google.url, None]

    # Redirect failed, read google screen info instead of website.
    if "&btnI" in response_redirect.url:
        return [response_redirect.url, None]
    
    # Redirects to other google products (like youtube) do not need to be split.
    if "q=" not in response_redirect.url:
        return [response_google.url, response_redirect.url]

    [_, redirect_url] = response_redirect.url.split("q=")

    return [response_google.url, redirect_url]
 

def fetch_command(keywords: str) -> str:
    [google_url, redirect_url] = fetch_link_for_keywords_google(keywords)

    response = None

    # Temporary
    if (redirect_url):
        decoded_url = urllib.parse.unquote(redirect_url)

        response = fetch_readable_html(decoded_url)
    
    if not response :
        # raise Exception(f"FETCH CMD: got non 200 error from website {decoded_url}")
        response = fetch_readable_html(google_url)
        return ['google fallback', response]

    return [decoded_url, response]

def fetch_command_safe(keywords: str) -> str:
    try: 
        return fetch_command(keywords)
    except Exception as e:
        return [None, f"Error: {e}"]

if __name__ == "__main__":
    try: 
        response = fetch_command("2022 f1 world champion")
        print(response)
    except Exception as e:
        print(e)
