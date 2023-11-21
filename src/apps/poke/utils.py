import json
import logging

import numpy as np
import redis
import requests

logging.basicConfig(filename="app.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def get_all_berry():
    """
    Fetches all berry items available from the PokeAPI.

    Returns:
    - list: A list containing dictionaries of berry items available in the PokeAPI.
            Each dictionary contains information about a single berry item.
            Example format: [{'name': 'cheri', 'url': 'https://pokeapi.co/api/v2/berry/1/'}, ...]
    """
    base_url = "https://pokeapi.co/api/v2/berry/"
    all_items = []

    while base_url:
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            all_items.extend(data["results"])
            base_url = data["next"]
        else:
            base_url = None

    return all_items


def get_all_berries_info():
    """
    This function fetches information about berries from the PokeAPI or a Redis cache if available.
    It retrieves berry names and their corresponding growth times.

    Returns:
    - tuple: A tuple containing two lists:
        - List of strings: Names of berries available in the PokeAPI.
        - List of integers: Growth times (in minutes) for each corresponding berry.
          Growth times are fetched from the PokeAPI if not available in the cache.

    Notes:
    - This function interacts with Redis to store and retrieve cached data for berries and growth times.
    - In case of missing or incomplete data in the cache, it makes requests to the PokeAPI for specific berry details.
    - If errors occur during API requests or JSON parsing, they are logged with appropriate messages.
    """

    # Check if berries list is on redis
    redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)
    berries = redis_client.get("berries")

    if berries:
        berries = json.loads(berries)
    else:
        berries = get_all_berry()
        if berries:
            redis_client.set("berries", json.dumps(berries))
        else:
            return None

    names = [berry["name"] for berry in berries]

    # Check if growth_times list is on redis
    growth_times = redis_client.get("growth_times")

    if growth_times:
        growth_times = json.loads(growth_times)
    else:
        growth_times = []
        for berry in berries:
            try:
                response = requests.get(berry["url"])
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    growth_times.append(data["growth_time"])
            except requests.RequestException as e:
                logging.error(f"Error in request for {berry['name']}: {e}")
            except KeyError as e:
                logging.error(f"Key not found in JSON response for {berry['name']}: {e}")

        redis_client.set("growth_times", json.dumps(growth_times))

    return names, growth_times


def generate_statistics(growth_times):
    """
    Calculates statistical measures for a given array of growth times.

    Args:
    - growth_times (list): A list containing growth times (in cicles) for berries.

    Returns:
    - dict: A dictionary containing various statistical measures calculated from the growth times.
        - "min_growth_time": Minimum growth time among the provided data.
        - "median_growth_time": Median growth time among the provided data.
        - "max_growth_time": Maximum growth time among the provided data.
        - "variance_growth_time": Variance of growth times.
        - "mean_growth_time": Mean (average) of growth times.
        - "frequency_growth_time": Dictionary containing frequencies of each unique growth time.
    """
    numbers_array = np.array(growth_times)

    minimum = np.min(numbers_array)

    median = float(np.median(numbers_array))

    maximum = float(np.max(numbers_array))

    variance = float(np.var(numbers_array))

    mean = float(np.mean(numbers_array))

    unique_elements, frequency = np.unique(numbers_array, return_counts=True)

    element_frequency = dict(zip(unique_elements, frequency))

    return {
        "min_growth_time": minimum,
        "median_growth_time": median,
        "max_growth_time": maximum,
        "variance_growth_time": variance,
        "mean_growth_time": mean,
        "frequency_growth_time": element_frequency,
    }
