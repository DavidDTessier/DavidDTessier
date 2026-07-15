import time
import re
import feedparser

RSS_URL = "https://blog.daviddtessier.ca/rss.xml"
MARKER_START = "<!-- BLOG-POST-LIST:START -->"
MARKER_END = "<!-- BLOG_POST-LIST:END -->"

def get_latest_posts(limit=5):
    """Fetches the latest blog posts from the RSS feed and returns them as a markdown list."""
    feed = feedparser.parse(RSS_URL)
    posts = feed.entries[:limit]
    md_list = ""
    for post in posts:
        # Format the date (e.g., "YYYY-MM-DD")
        pub_date = time.strftime("%Y-%m-%d", post.get('published_parsed', time.localtime()))

        # Create the markdown list item: date: [title](link)
        md_list += f"- {pub_date}: [{post.title}]({post.link})\n"

    return md_list

def update_readme(new_content):
    """Updates the README.md file with the new content between the specified markers."""
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    # Regex to replace content between the markers
    pattern = re.compile(
        f"{re.escape(MARKER_START)}(.*?){re.escape(MARKER_END)}", 
        re.DOTALL
    )

    replacement = f"{MARKER_START}\n{new_content}{MARKER_END}"
    new_readme = pattern.sub(replacement, readme)

    print(new_readme)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    update_readme(get_latest_posts())