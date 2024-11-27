import json
import urllib
from urllib.parse import urlparse

import requests

from config.config import NaverAPIIdentify
import urllib.request

SKIP_URL = {
    'tistory': ['tag', 'archive', 'category', 'rss', 'guestbook', 'manage', 'entry']
}

SITE_TYPE = {
    'com': {
        'tistory': 'TISTORY',
        'naver': 'NAVER',
    }
}

url_list = [
    'https://www.naver.com/',
    'https://www.naver.com/rules/service.html',
    'https://section.blog.naver.com/OfficialBlog.naver',
    'https://blog.naver.com/post/blog_use.htm',
    'https://section.blog.naver.com/HotTopicChallenge.naver',
    'https://section.blog.naver.com/PowerBlog.naver',
    'https://section.blog.naver.com/ThemePost.naver',
    'https://www.naver.com/rules/disclaimer.html',
    'https://help.naver.com/service/5593/contents/5043',
    'https://section.blog.naver.com/BlogHome.naver',
    'https://www.naver.com/rules/privacy.html',
    'https://section.blog.naver.com/thisMonthDirectory.naver',
    'https://section.blog.naver.com/PreviousThisMonthBlog.naver',
    'https://right.naver.com',
    'https://www.navercorp.com/',
]


def grab_url_list(search_word: str):
    client_id = NaverAPIIdentify.client_id
    client_secret = NaverAPIIdentify.client_secret

    enctext = urllib.parse.quote(search_word)
    url = "https://openapi.naver.com/v1/search/blog?query=" + enctext + "&display=5&sort=date"  # JSON 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    page = response.getcode()
    if page == 200:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body)
    else:
        print("Error Code:" + page)
        return None


def search_link(search_word: str):
    searched_url = set()
    try:
        page = grab_url_list(search_word)
    except requests.exceptions.HTTPError:
        raise

    items = page["items"]
    for item in items:
        url = item["link"]

        try:
            url = urlparse(url)
        except ValueError as e:
            print("Error: " + ' '.join(e.args))
            continue
        url_path = f'{url.scheme}://{url.netloc}{url.path}'

        if url_path not in url_list:
            searched_url.add(url_path)

        print()
    return searched_url


def get_base_url(url):
    url = urlparse(url)
    base_url = f'{url.scheme}://{url.netloc}'
    return base_url


def publish_embedded_links(search_word):
    embedded_links = search_link(search_word)

    return embedded_links


if __name__ == '__main__':
    # start_url = 'https://ksh-coding.tistory.com/144'
    start_url = 'https://section.blog.naver.com'
    publish_embedded_links(start_url)
