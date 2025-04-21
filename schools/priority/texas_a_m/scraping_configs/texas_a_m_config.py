from scraper_module.config import *

config = SpiderConfig(
    name="texas_am_university",
    start_url="https://catalog.tamu.edu/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://*[@id="/"]',
        link_selector='xpath://a[starts-with(@aria-label, "Page")]'
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://*[@id="coursestextcontainer"]/div',
            repeating_selector="div",
            fields={
                "title": 'xpath:*[@class="courseblocktitle"]//text()',
                "description": 'xpath:*[@class="courseblockdesc"]//text()join'
            },
            num_required=1
        )
    ]
)