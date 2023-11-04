import aiohttp
import asyncio
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


async def parse_page(url):
    soup = await get_soup(url)

    news_titles = []
    for news_item in soup.find_all("div", class_="article"):
        title = news_item.find("a").text.strip()
        news_titles.append(title)

    return news_titles


async def main():
    base_url = "https://itproger.com/news/"
    # num_pages = 5  # Количество страниц для парсинга

    soup = await get_soup(base_url)
    num_pages = await get_num_pages(soup)
    tasks = [parse_page(f"{base_url}page-{page}") for page in range(1, int(num_pages) + 1)]
    results = await asyncio.gather(*tasks)

    all_news_titles = []
    for result in results:
        all_news_titles.extend(result)

    for i, title in enumerate(all_news_titles, start=1):
        print(f"{i}. {title}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
