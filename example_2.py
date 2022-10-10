import json
import py_chartmetric_api

arr = {}  # dictionary containing the request results
OUTPUT_FILENAME = "test.json"


COUNTRY_CODE = "CA"
URL_1 = "https://api.chartmetric.com/api/artist/list/filter"


artists = (
    py_chartmetric_api.utility.get_data_from_chartmetrics(URL_1, {"offset": 0, "limit": 10})
    .json()
    .get("obj")
    .get("obj")
)

py_chartmetric_api.artist.get_artist_metadata("111")

for artist in artists:
    artist_id = artist["cm_artist"]

    URL_2 = "https://api.chartmetric.com/api/artist/" + artist_id

    metadata = py_chartmetric_api.artist.get_artist_metadata(artist_id).get("artist_metadata")

    artist_data = {artist.get("cm_artist"): artist | metadata}
    arr.update(artist_data)


data = arr
with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
    json.dump(arr, f)
