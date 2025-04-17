import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_hackernews(pages=3):
    base_url = "https://news.ycombinator.com/"
    posts = []

    for page in range(1, pages + 1):
        url = f"{base_url}news?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select("tr.athing")
        for item in items:
            title_tag = item.select_one("span.titleline a")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = urljoin(base_url, title_tag['href'])

            subtext_row = item.find_next_sibling("tr")
            score_tag = subtext_row.select_one(".score")
            score = int(score_tag.text.split()[0]) if score_tag else 0

            posts.append({
                "title": title,
                "link": link,
                "score": score
            })

    return posts

def search_posts(posts, query):
    query = query.lower()
    matches = [post for post in posts if query in post["title"].lower()]
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

def display_results(results):
    if not results:
        print("No results found.")
        return

    for i, post in enumerate(results, 1):
        print(f"{i}. {post['title']}")
        print(f"   🔗 {post['link']}")
        print(f"   📈 Score: {post['score']}\n")

def hn(query):
    print("🔎 HackerNews Search Engine (multi-page)")

    print("Scraping Hacker News... Please wait.")
    posts = scrape_hackernews(pages=8)  # You can adjust page count here
    results = search_posts(posts, query)
    display_results(results)

