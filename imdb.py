import requests
import json

def get_more_like_this(imdb_id):
    url = "https://api.graphql.imdb.com/"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.imdb.com",
        "Referer": f"https://www.imdb.com/title/{imdb_id}/"
    }

    query = {
        "query": """
        query MoreLikeThis($id: ID!) {
          title(id: $id) {
            moreLikeThisTitles(first: 12) {
              edges {
                node {
                  id
                  titleText {
                    text
                  }
                }
              }
            }
          }
        }
        """,
        "variables": {"id": imdb_id}
    }

    response = requests.post(url, headers=headers, json=query)
    response.raise_for_status()

    data = response.json()

    recommendations = []

    edges = data["data"]["title"]["moreLikeThisTitles"]["edges"]

    for item in edges:
        node = item["node"]
        recommendations.append({
            "title": node["titleText"]["text"],
            "id": node["id"]
        })

    return recommendations



watched = []

with open('imdb_list.json', 'r') as file:
    new_shows = json.load(file)


reccommendations = {}
titles = {}

for a in new_shows.keys():
  data = new_shows[a]
  imdb_id = a

  rating = 0
  if 'rating' in data.keys():
    rating = data['rating']
  
  modifier = rating

  if a not in reccommendations.keys(): 
    reccommendations[a] = modifier
    titles[a] = data['title']
  else:
    reccommendations[a] += modifier
  
  recs = get_more_like_this(imdb_id)

  for rec in recs:
    title = rec["title"]
    imdb_id = rec["id"]
    if imdb_id not in reccommendations.keys():
      reccommendations[imdb_id] = modifier
      titles[imdb_id] = title
    else:
      reccommendations[imdb_id] += modifier



  with open('imdb_recommendations.txt', 'w') as f:
    for a in reccommendations.keys():
      title = titles[a]
      f.write(f"{title} ({a}): {reccommendations[a]}\n")



clean_recs = {k: v for k, v in reccommendations.items() if k not in new_shows.keys()}

sorted_recommendations = sorted(clean_recs.items(), key=lambda x: x[1], reverse=True)
with open('imdb_recommendations.txt', 'w') as f:
    for imdb_id, score in sorted_recommendations:
        title = titles[imdb_id]
        f.write(f"{title} ({imdb_id}): {score}\n")



