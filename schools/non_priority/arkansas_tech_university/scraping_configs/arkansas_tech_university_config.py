from scraper_module.config import *

config = SpiderConfig(
    name="atu",
    start_url="https://catalog.atu.edu/courses/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://*[@id="textcontainer"]/div',
        link_selector='xpath:/ul/li/a/@href',
        target_page_selector='html', # Target page to scrape
        max_depth = 1
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://div[@class="sc_sccoursedescs"]',
            repeating_selector="div",
            fields={
                "title": 'xpath:div[@class="cols noindent"]/span//text()',
                "description": 'xpath:div[@class="noindent"]/div[@class="courseblockextra noindent"]//text()join'
            },
            num_required=1
        )
    ]
)