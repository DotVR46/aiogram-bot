import aiohttp
import asyncio
from bs4 import BeautifulSoup

from database.connection import session, Post


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
        title = news_item.find("span").text
        img = news_item.find("img").get("src")[1:]
        full_link = (
            f"{base_url}news/{link}" if "tasks" not in link else f"{base_url}{link[1:]}"
        )
        if full_link not in existing_links:
            item = {
                "post_url": full_link,
                "image_url": f"{base_url}{img}",
                "post_title": title,
            }
            news_links.append(item)
            existing_links.add(full_link)

    return news_links


async def main():
    base_url = "https://itproger.com/"

    async with session:
        existing_posts = await session.execute(Post.__table__.select())
        existing_links = set(row[0] for row in existing_posts)

        soup = await get_soup(base_url + "news/")
        num_pages = await get_num_pages(soup)

        tasks = [
            parse_page(f"{base_url}news/page-{page}", base_url, existing_links)
            for page in range(1, int(num_pages) + 1)
        ]
        results = await asyncio.gather(*tasks)

        for result in results:
            for post in result:
                new_post = Post(post_url=post["post_url"], image_url=post["image_url"], post_title=post["post_title"])
                session.add(new_post)

        await session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
