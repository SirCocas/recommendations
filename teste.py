import requests
import html
from bs4 import BeautifulSoup

BASE_URL = "https://www.anime-planet.com"

def extract_title(entry_html):
    soup = BeautifulSoup(entry_html, "html.parser")
    tag = soup.find("h5", class_="theme-font")
    return tag.get_text(strip=True) if tag else None




def get_recs_from_url(rec_page_url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    rec_page = requests.get(rec_page_url, headers=headers)
    rec_page.raise_for_status()
    rec_soup = BeautifulSoup(rec_page.text, "html.parser")

    # Step 4: Extract titles and URLs
    recommendations = []



    for rec in rec_soup.select('div.recEntry'):
        link = rec.find("a", href=True)
        img = rec.find("img", alt=True)
        if not link or not img:
            continue

        title = img["alt"].strip()
        href = link["href"].strip()
        recommendations.append({
            "title": title,
            "url": f"{BASE_URL}{href}",
        })
    return recommendations


def get_recommendations(anime_url):

    rec_page_url = anime_url+"/recommendations"

    recs = get_recs_from_url(rec_page_url)

    page = 2

    while True:
        last = recs[-1]
        rec_page_url = anime_url+"/recommendations?page="+str(page)
        new_recs = get_recs_from_url(rec_page_url)
        if (new_recs[-1]['title'] == last['title']):
            break
        else:
            recs.extend(new_recs)
            page += 1

    return(recs)

    



if __name__ == "__main__":
    url = "https://www.anime-planet.com/anime/naruto"
    recs = get_recommendations(url)

    print(f"Recommendations for {url}:")
    for r in recs:
        print(f"- {r['title']}: {r['url']}")
