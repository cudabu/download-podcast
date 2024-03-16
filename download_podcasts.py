from pathlib import Path
import feedparser
import requests
from typing import Optional

def create_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def download_file(url: str, filename: Path, count: int, total: int) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        with filename.open('wb') as file:
            file.write(response.content)
        print(f"[{count}/{total}] Saved: {filename}")
    except requests.RequestException as e:
        print(f"[{count}/{total}] Failed to download {url}. Reason: {e}")

def get_mp3_link(entry) -> Optional[str]:
    for link in entry.links:
        if link['type'] == 'audio/mpeg':
            return link['href']
    return None

def main(rss_feed_url: str, download_location: str) -> None:
    download_path = Path(download_location)
    create_directory(download_path)

    feed = feedparser.parse(rss_feed_url)
    total_entries = len(feed.entries)

    for count, entry in enumerate(feed.entries, start=1):
        title = entry.title
        mp3_url = get_mp3_link(entry)

        if mp3_url:
            safe_title = title.replace("/", "-").replace("\\", "-")
            filename = download_path / f"{safe_title}.mp3"

            if not filename.exists():
                print(f"[{count}/{total_entries}] Downloading: {title}")
                download_file(mp3_url, filename, count, total_entries)
            else:
                print(f"[{count}/{total_entries}] File already exists: {filename}")
        else:
            print(f"MP3 URL not found for: {title}")

if __name__ == "__main__":
    rss_feed_url= "https://roosterteeth.supportingcast.fm/content/eyJ0IjoicCIsImMiOiIxNDA2IiwidSI6IjEyOTI3NzIiLCJkIjoiMTYzMTU1MzU2NiIsImsiOjI2MX18NDBkMzExYzZjMzVmYTc5NDYzZmU2Yjc4NTgzZDdjZjgyMTIxYjY5MWJjZGQ3NTY2NGU4NWUxYmU2ZDcxYWQzMA.rss"
    download_location = "/mnt/c/Users/cudabu/Downloads/totsd_podcast"
    main(rss_feed_url, download_location)