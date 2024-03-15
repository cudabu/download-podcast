import feedparser
import requests
import os

rss_feed_url= "https://roosterteeth.supportingcast.fm/content/eyJ0IjoicCIsImMiOiIxNDA2IiwidSI6IjEyOTI3NzIiLCJkIjoiMTYzMTU1MzU2NiIsImsiOjI2MX18NDBkMzExYzZjMzVmYTc5NDYzZmU2Yjc4NTgzZDdjZjgyMTIxYjY5MWJjZGQ3NTY2NGU4NWUxYmU2ZDcxYWQzMA.rss"
download_location = "/mnt/c/Users/cudabu/Downloads/totsd_podcast"

if not os.path.exists(download_location):
    os.makedirs(download_location)

feed = feedparser.parse(rss_feed_url)

for entry in feed.entries:
    title = entry.title
    mp3_url = None
    for link in entry.links:
        if link['type'] == 'audio/mpeg':
            mp3_url = link['href']
            break

    if mp3_url is not None:
        print(f"Downloading: {title}")
        safe_title = title.replace("/", "-").replace("\\", "-")
        filename = os.path.join(download_location, f"{safe_title}.mp3")

    if not os.path.exists(filename):
        response = requests.get(mp3_url)

        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Saved: {filename}")
    else:
        print(f"File already exists: {filename}")
else:
    print(f"MP3 URL not found for: {title}")