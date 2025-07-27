import httpx
import re
from bs4 import BeautifulSoup


def extract_valid_essay_urls(start_url: str, client: httpx.Client) -> set[str]:
    """
    Extract valid URLs from the start url link as a set of strings.
    Returns an empty set of no valid urls are found else it returns
    """

    valid_urls = set()

    try:
        total_valid = 0
        response = client.get(start_url)

        if response.status_code != 200:
            raise Exception(f"The website {start_url} is not reachable!")

        soup = BeautifulSoup(response.text, "html5lib")

        article_links = soup.find_all(
            "a", href=re.compile(r"/college-essay-examples/.*")
        )
        # Inspect element and get this.
        if not article_links:
            print("No article links found.")
            return valid_urls

        for link in article_links:
            if "class" in link.attrs and link["class"] == ["blog-categories"]:
                continue

            complete_url = "https://" + client.get(base_url).url.host + link["href"]
            valid_urls.add(complete_url)
            total_valid += 1

        print(f"Detected {len(valid_urls)} unique URLs out of {total_valid} valid URLs")

    except Exception as e:
        print(f"Error processing base URL {start_url}: {e}")
        return valid_urls

    return valid_urls


def extract_essay_body(client: httpx.Client, link: str) -> str:
    """
    Extracts the body of the essay page using the currently known structure of the html document
    """
    try:
        response = client.get(link)
    except httpx.InvalidURL:
        raise httpx.RequestError("{link} is not a vaid")

    if response.status_code != 200:
        raise httpx.RequestError("{link} is not accessible")

    body = BeautifulSoup(response.text, "html5lib").find("main", id="page").text

    return body
