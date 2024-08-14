import feedparser

def get_headlines(rss_url):
    """
    @returns a list of titles from the rss feed located at `rss_url`
    """
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    # Extract titles from the feed entries
    titles = [entry.title for entry in feed.entries]
    
    return titles

# Example usage
google_news_url = "https://news.google.com/news/rss"
print(get_headlines(google_news_url))
