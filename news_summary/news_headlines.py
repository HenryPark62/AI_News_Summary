import feedparser

def get_latest_headlines(feed_url="https://www.mk.co.kr/rss/40300001/", limit=10):
    feed = feedparser.parse(feed_url)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:limit]]
