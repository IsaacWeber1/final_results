from scraper_module.config import *

config = SpiderConfig(
    name="iowa_state",
    start_url="https://catalog.iastate.edu/azcourses/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://*[@id="atozindex"]',
        link_selector="xpath:ul/li/a/@href",
        target_page_selector='' # Target page to scrape
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://*[@id="courseinventorycontainer"]/div',
            repeating_selector="div",
            fields={
                "title": 'xpath://*[@id="courseinventorycontainer"]/div/div[2]/div[1]/a/strong//text()join',
                "description": 'xpath://*[@id="courseinventorycontainer"]/div/div[2]/div[2]/p[2]/text()[1]'
            },
            num_required=1
        )
    ]
)