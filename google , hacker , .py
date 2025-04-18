import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

# Download necessary resources for VADER sentiment analysis
nltk.download('vader_lexicon')

# ---------- SENTIMENT ANALYSIS ----------
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# ---------- SAVE TO CSV ----------
def save_to_csv(results, filename, include_score=False):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if include_score:
            writer.writerow(["Title", "Link", "Score", "Sentiment"])
            for post in results:
                sentiment = analyze_sentiment(post['title'])
                writer.writerow([post['title'], post['link'], post['score'], sentiment])
        else:
            writer.writerow(["Title", "Link", "Sentiment"])
            for post in results:
                sentiment = analyze_sentiment(post['title'])
                writer.writerow([post['title'], post['link'], sentiment])
    print(f"✅ Saved to {filename}")

# ---------- HACKER NEWS ----------
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

            posts.append({"title": title, "link": link, "score": score})

    return posts

def search_hn(query):
    print("🔍 Scraping Hacker News...")
    posts = scrape_hackernews(pages=5)
    results = [p for p in posts if query.lower() in p['title'].lower()]
    results.sort(key=lambda x: x["score"], reverse=True)
    save_to_csv(results, f"hackernews_results_{query}.csv", include_score=True)

# ---------- GOOGLE TRENDS ----------
def search_google_trends(query):
    print("🔍 Adding Google Trends link...")
    url = f"https://trends.google.com/trends/explore?q={query}"
    results = [{"title": f"Explore trends for '{query}'", "link": url}]
    save_to_csv(results, f"google_trends_{query}.csv")

# ---------- STATISTA ----------
def search_statista(query):
    print("🔍 Scraping Statista...")
    url = f"https://www.statista.com/search/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select(".search-result-item__title"):
        a_tag = item.find("a")
        if not a_tag:
            continue
        title = a_tag.get_text(strip=True)
        link = urljoin("https://www.statista.com", a_tag["href"])
        results.append({"title": title, "link": link})

    save_to_csv(results, f"statista_results_{query}.csv")

# ---------- MAIN ----------
def search_all(query):
    print(f"\n🔎 Multi-Source Search for: {query}\n")
    search_hn(query)
    search_google_trends(query)
    search_statista(query)
    print("\n🎯 Search completed.")

# ---------- RUN ----------
if __name__ == "__main__":
    query = input("Enter search query: ")
    search_all(query)