import os
import urllib.request
import json

API_KEY = os.environ.get("TMDB_API_KEY")
BASE = "https://" + "api.themoviedb.org/3/"
IMG = "https://" + "image.tmdb.org/t/p/w500"
YT = "https://" + "www." + "youtube.com" + "/watch?v="

def fetch_tmdb(endpoint):
    url = f"{BASE}{endpoint}?api_key={API_KEY}&language=ro-RO"
    req = urllib.request.urlopen(url)
    return json.loads(req.read().decode("utf-8")).get("results", [])

def get_trailer(media_type, item_id):
    url = f"{BASE}{media_type}/{item_id}/videos?api_key={API_KEY}"
    req = urllib.request.urlopen(url)
    videos = json.loads(req.read().decode("utf-8")).get("results", [])
    for v in videos:
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            return f"{YT}{v['key']}"
    return None

lines = ["#EXTM3U"]

for movie in fetch_tmdb("trending/movie/week"):
    title = movie.get("title", "Film Nou").replace(",", " ")
    poster = f"{IMG}{movie['poster_path']}" if movie.get("poster_path") else ""
    trailer = get_trailer("movie", movie["id"])
    if trailer:
        lines.append(f'#EXTINF:-1 tvg-logo="{poster}" group-title="Filme Noi (Trailere)",{title}')
        lines.append(trailer)

for tv in fetch_tmdb("trending/tv/week"):
    name = tv.get("name", "Serial Nou").replace(",", " ")
    poster = f"{IMG}{tv['poster_path']}" if tv.get("poster_path") else ""
    trailer = get_trailer("tv", tv["id"])
    if trailer:
        lines.append(f'#EXTINF:-1 tvg-logo="{poster}" group-title="Seriale Noi (Trailere)",{name}')
        lines.append(trailer)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
