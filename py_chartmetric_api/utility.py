"""This module contains utility functions to interact with chartmetrics
"""
import time
import requests
import dotenv


config = dotenv.dotenv_values(".env")


def get_refresh_token():
    """obtains a refresh token if needed

    Returns:
        Response: the refresh token
    """

    access_token = config["ACCESS_TOKEN"]

    # Get the current epoch time in seconds and compare with the token expiry date.
    # If less than 2 minutes before access token expiration, request a new token
    # Otherwise, return the current token
    epoch_time = int(time.time())
    if epoch_time + 120 >= int(config["TOKEN_EXPIRY_DATE"]):

        url = "https://api.chartmetric.com/api/token"
        data = {"refreshtoken": config["REFRESH_TOKEN"]}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, json=data, headers=headers, timeout=60)

        access_token = response.json().get("token")

        # update the .env file with the new values.
        dotenv.set_key(".env", "ACCESS_TOKEN", access_token)
        dotenv.set_key(".env", "TOKEN_EXPIRY_DATE", str(epoch_time + 3600))

    return access_token


def get_data_from_chartmetrics(url: str, params: str = None):
    """requests and returns data from chartmetrics

    Parameters:
        url (str): url of the api route to usee
        param (str): extra parameters for the request

    Returns:
        Response: response from the api
    """

    if params is None:
        params = {}
    token = {"authorization": "Bearer " + get_refresh_token()}

    response = requests.get(url=url, params=params, headers=token, timeout=60)
    return response
