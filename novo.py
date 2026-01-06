import json
import requests
import html
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.anime-planet.com"


def get_recs_from_url(rec_page_url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    time.sleep(2)  # Be polite and avoid overwhelming the server
    try:
        print('Fetching recommendations from:', rec_page_url)
        rec_page = requests.get(rec_page_url, headers=headers)
        rec_page.raise_for_status()
        rec_soup = BeautifulSoup(rec_page.text, "html.parser")
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return []
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


watched = []

with open('new_shows.json', 'r') as file:
    new_shows = json.load(file)

#print(new_shows)

recommendations = {}

for show in new_shows.keys():
    data = new_shows[show]
    url = data['url']

    recommendations_small = []
    if 'recommends' in data.keys():
        recommendations_small = data['recommends']

    status = None
    if 'state' in data.keys():
        status = data['state'] 

    rating = 0
    if 'rating' in data.keys():
        rating = data['rating'] 

    #print(data)

    modifier = rating
    if status == 'watching':
        modifier += 1
        watched.append(show)
    elif status == 'completed':
        modifier += 2
        watched.append(show)
    
    #add the show itself to the list
    if show not in recommendations.keys(): 
        recommendations[show] = modifier
    else:
        recommendations[show] += modifier


    # add manual recommendations
    for rec in recommendations_small:
        if rec not in recommendations.keys():
            recommendations[rec] = modifier
        else:
            recommendations[rec] += modifier


    #add automatic recommendations

    recc_url = url + '/recommendations'

    tmp = get_recs_from_url(recc_url)
    page = 2

    while True:
        last = tmp[-1]
        rec_page_url = url+"/recommendations?page="+str(page)
        new_recs = get_recs_from_url(rec_page_url)
        if (new_recs[-1]['title'] == last['title']):
            break
        else:
            tmp.extend(new_recs)
            page += 1
    
    for elem in tmp:
        elem_title = elem['title']
        if elem_title not in recommendations.keys():
            recommendations[elem_title] = modifier
        else:
            recommendations[elem_title] += modifier

    with open("recommendations.txt", "w", encoding="utf-8") as f:
        for title, score in sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            f.write(f"{title}: {score}\n")

    


recommendations = {k: v for k, v in recommendations.items() if k not in watched}
with open("recommendations.txt", "w", encoding="utf-8") as f:
    for title, score in sorted(
        recommendations.items(),
        key=lambda x: x[1],
        reverse=True
   ):
       f.write(f"{title}: {score}\n")