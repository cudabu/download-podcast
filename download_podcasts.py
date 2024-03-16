from pathlib import Path
import feedparser
import requests
from typing import Optional

class PodcastDownloader:
    def __init__(self, rss_feed_url: str, download_location: str):
        self.rss_feed_url = rss_feed_url
        self.download_path = Path(download_location)
        self.total_entries = 0
        self.create_directory()

    
    def create_directory(self) -> None:
        self.download_path.mkdir(parents=True, exist_ok=True)


    def download_file(self, url: str, filename: Path, count: int) -> None:
        try:
            response = requests.get(url)
            response.raise_for_status() # raises an HTTP error for unsuccessful statuses.
            with filename.open('wb') as file:
                file.write(response.content)
            print(f"({count}/{self.total_entries}) Saved: {filename}")
        except requests.RequestException as e:
            print(f"({count}/{self.total_entries}) Failed to download {url}. Reason: {e}")

    @staticmethod
    def get_mp3_link(entry) -> Optional[str]:
        for link in entry.links:
            if link['type'] == 'audio/mpeg':
                return link['href']
        return None
    
    def download_episodes(self) -> None:
        feed = feedparser.parse(rss_feed_url)
        self.total_entries = len(feed.entries)

        for count, entry in enumerate(feed.entries, start=1):
            title = entry.title
            mp3_url = self.get_mp3_link(entry)

            if mp3_url:
                safe_title = title.replace("/", "-").replace("\\", "-")
                filename = self.download_path / f"{safe_title}.mp3"

                if not filename.exists():
                    print(f"[{count}/{total_entries}] Downloading: {title}")
                    self.download_file(mp3_url, filename, count)
                else:
                    print(f"({count}/{self.total_entries}) File already exists: {filename}")
            else:
                print(f"({count}/{self.total_entries})MP3 URL not found for: {title}")

if __name__ == "__main__":
    rss_feed_url= "https://roosterteeth.supportingcast.fm/content/eyJ0IjoicCIsImMiOiIxNDA2IiwidSI6IjEyOTI3NzIiLCJkIjoiMTYzMTU1MzU2NiIsImsiOjI2MX18NDBkMzExYzZjMzVmYTc5NDYzZmU2Yjc4NTgzZDdjZjgyMTIxYjY5MWJjZGQ3NTY2NGU4NWUxYmU2ZDcxYWQzMA.rss"
    download_location = "/mnt/c/Users/cudabu/Downloads/totsd_podcast"
    downloader = PodcastDownloader(rss_feed_url, download_location)
    downloader.download_episodes()