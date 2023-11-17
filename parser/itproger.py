import os

import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup


async def get_soup(url) -> BeautifulSoup():
    html = await fetch_url(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup


async def get_num_pages(soup):
    pages = soup.find("div", class_="pagination")
    last_page = pages.find_all("a")[-2].text

    return last_page


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_page(url, base_url, existing_links):
    soup = await get_soup(url)

    news_links = []
    for news_item in soup.find_all("div", class_="article"):
        link = news_item.find("a").get("href")
        img = news_item.find("img").get("src")[1:]
        full_link = (
            f"{base_url}news/{link}"
            if "tasks" not in link
            else f"{base_url}{link[1:]}"
        )
        if full_link not in existing_links:
            item = [full_link, f"{base_url}{img}"]
            news_links.append(item)
            existing_links.add(full_link)

    return news_links


# TODO: Сохранять новые посты сразу в БД
# TODO: Парсить только свежие посты. Проверять дату каждого поста и сравнивать с последней
async def main():
    base_url = "https://itproger.com/"
    # num_pages = 5  # Количество страниц для парсинга
    existing_links = set()

    # Load existing links from the CSV file
    if os.path.exists("itproger.csv"):
        with open("itproger.csv", "r") as file:
            reader = csv.reader(file)
            existing_links = set(row[0] for row in reader)

    soup = await get_soup(base_url + "news/")
    num_pages = await get_num_pages(soup)
    tasks = [
        parse_page(f"{base_url}news/page-{page}", base_url, existing_links)
        for page in range(1, int(num_pages) + 1)
    ]
    results = await asyncio.gather(*tasks)

    all_news_links = []
    for result in results:
        all_news_links.extend(result)

    # for i, link in enumerate(all_news_links, start=1):
    #     print(f"{i}. {base_url}{link}")
    with open("itproger.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_news_links)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
