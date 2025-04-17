import requests
from bs4 import BeautifulSoup
from googlesearch import search
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

# Download VADER once
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return compound, label

def fetch_quora_links(query, num_links=10):
    search_query = f"site:quora.com {query}"
    return list(search(search_query, num_results=num_links))

def extract_quora_titles(links):
    results = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    for link in links:
        try:
            response = requests.get(link, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else "No title"

            score, sentiment = analyze_sentiment(title)

            results.append({
                "title": title,
                "link": link,
                "sentiment": sentiment,
                "score": (int) (score * 1000)
            })
        except Exception as e:
            print(f"⚠️ Failed to fetch {link}: {e}")
    return results

def display_results(results):
    if not results:
        print("No results found.")
        return
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}")
        print(f"   🔗 {item['link']}")
        print(f"   😊 Sentiment: {item['sentiment']} (Score: {item['score']})\n")

def save_results_to_csv(results, filename="quora_search_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'link', 'score' ,'sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in results:
            writer.writerow(item)
    print(f"✅ Results saved to {filename}")

def qv(query):
    # print("🔎 Quora Sentiment Search Tool")
    # while True:
        # query = input("\nEnter a search query (or 'exit' to quit): ").strip()
        # if query.lower() == 'exit':
        #     break

        print("🔍 Searching Quora...")
        links = fetch_quora_links(query)
        results = extract_quora_titles(links)

        display_results(results)
        save_results_to_csv(results)


