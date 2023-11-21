import json

import numpy as np
import redis
import requests


def get_all_berry():
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
    # Check if berries list is on redis
    redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)
    berries = redis_client.get("berries")

    if berries:
        berries = json.loads(berries)
    else:
        berries = get_all_berry()
        redis_client.set("berries", json.dumps(berries))

    names = [berry["name"] for berry in berries]

    # Check if growth_times list is on redis
    growth_times = redis_client.get("growth_times")

    if growth_times:
        growth_times = json.loads(growth_times)
    else:
        growth_times = []
        for berry in berries:
            response = requests.get(berry["url"])
            if response.status_code == 200:
                data = response.json()
                growth_times.append(data["growth_time"])

        redis_client.set("growth_times", json.dumps(growth_times))

    return names, growth_times


def generate_statistics(growth_times):
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
