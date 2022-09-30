import json
import py_chartmetric_api


arr = {}  # dictionary containing the request results
OUTPUT_FILENAME = "artists.json"


arr = arr | py_chartmetric_api.artist.get_artists_with_filters(0, 1, {"firstReleaseDaysAgo": "30"})
arr = arr | py_chartmetric_api.artist.get_artists_by_stats("sp_followers", 1000, 100000, 300)


data = arr
with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
    json.dump(data, f)
