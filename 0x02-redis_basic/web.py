#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import requests
import redis


def get_page(url: str) -> str:
    """Fetch HTML content of a given URL."""
    redis_client = redis.Redis()

    url_count_key = f"count:{url}"
    redis_client.incr(url_count_key)

    cached_content = redis_client.get(url)
    if cached_content:
        return cached_content.decode()

    response = requests.get(url)
    html_content = response.text

    redis_client.setex(url, 10, html_content)

    return html_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
