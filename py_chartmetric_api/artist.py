"""This module contains functions to retrieve artist data from chartmetrics
"""
import requests
from . import utility


def get_artists_with_filters(
    offset: str,
    limit: int,
    params: str,
):
    """requests and returns artists depending on filters. The sum of offset and limit cannot be over 10000.

    Parameters:
        param (str): extra parameters for the request
        offset (str): offset for results
        limit (int): result limit

    Returns:
        Response: response from the api
    """
    url = "https://api.chartmetric.com/api/artist/list/filter"
    if offset + limit > 10000:
        if offset > 10000:
            raise ValueError("sum of offset and limit must be below 10000")
        if limit > 10000:
            limit = 10000 - offset
        else:
            limit = offset + limit - 10000

    try:
        params = params | {"offset": offset, "limit": limit}
        response = utility.get_data_from_chartmetrics(url, params)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error
    if response.status_code != 200:
        raise ConnectionError(response.text)
    return {"artists_with_filters": response.json().get("obj").get("obj")}


def get_artists_by_stats(metric_type: str, min_value: int, max_value: int, limit: int, params: str = None):
    """requests and returns artists data depending on a performance metric. The type of metric must be specified, as do the min and max value.

    A maximum of 200 entries can be returned but multiple requests will be made up to the provided limit, up to 100000 results or until all results have been returned.

    Parameters:
        type (str): performance metric (see https://api.chartmetric.com/apidoc/#api-Artist-getArtistListByStats)
        min (int): lower limit for performance metric filter
        max (int): lower limit for performance metric filter
        limit (int): result count limit
        param (str): extra parameters for the request

    Returns:
        Response: response from the api
    """
    url = "https://api.chartmetric.com/api/artist/list/filter"
    more_results = 1
    i = 0
    results = []

    if params is None:
        params = {}

    params = {"min": min_value, "max": max_value} | params

    while more_results == 1:
        url = "https://api.chartmetric.com/api/artist/" + metric_type + "/list"

        response = utility.get_data_from_chartmetrics(url, params | {"offset": str(200 * i), "limit": 200})

        data = response.json()
        results = results + data.get("obj").get("data")
        # print(i)
        # print(data.get("obj").get("data"))
        # print(data.get("obj").get("length"))

        i += 1
        if data.get("obj").get("length") < 200:
            more_results = 0
        if len(results) >= limit:
            more_results = 0
    # print(results)
    return {"artists_by_stats": results}


def get_artist_metadata(artist_id: str):
    """requests and returns metadata for a given artist

    Parameters:
        artist_id (str): chartmetric id for the requested artist

    Returns:
        Response: response from the api
    """
    url = "https://api.chartmetric.com/api/artist/" + artist_id

    try:
        response = utility.get_data_from_chartmetrics(url)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error
    if response.status_code != 200:
        raise ConnectionError(response.text)
    return {"artist_metadata": response.json().get("obj")}
