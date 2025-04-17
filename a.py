import sqlite3

def fetch_all_posts():
    conn = sqlite3.connect("hackernews.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, link, score, sentiment FROM posts ORDER BY score DESC")
    rows = cursor.fetchall()

    if not rows:
        print("No posts found in the database.")
        return

    for i, row in enumerate(rows, 1):
        title, link, score, sentiment = row
        print(f"{i}. {title}")
        print(f"   🔗 {link}")
        print(f"   📈 Score: {score}")
        print(f"   😊 Sentiment: {sentiment}\n")

    conn.close()

if __name__ == "__main__":
    print("🗃️  Displaying all Hacker News posts from the database:\n")
    fetch_all_posts()
